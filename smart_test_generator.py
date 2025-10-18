import ast
import json
import os
import requests
from typing import Dict, List, Set, Tuple
from code_tracker import CodeTracker
from test_validator import TestValidator


class SmartTestGenerator:
    """Умный генератор тестов с анализом кода и адаптивным промптом"""

    def __init__(self, config_file: str = "test_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.tracker = CodeTracker(config_file)
        self.validator = TestValidator(config_file)

    def _load_config(self) -> Dict:
        """Загружает конфигурацию из файла"""
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def extract_functions_from_code(self, code: str) -> Set[str]:
        """Извлекает названия функций из кода"""
        functions = set()

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.add(node.name)

        except SyntaxError as e:
            print(f"Ошибка синтаксиса при парсинге кода: {e}")

        return functions

    def analyze_code_structure(self, code: str) -> Dict[str, Dict]:
        """Анализирует структуру кода и возвращает детальную информацию о функциях"""
        analysis = {
            "functions": {},
            "dependencies": {},
            "data_structures": {},
            "output_patterns": {},
        }

        try:
            tree = ast.parse(code)

            # Анализируем функции
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_name = node.name
                    analysis["functions"][func_name] = self._analyze_function(
                        node, code
                    )

            # Анализируем зависимости и структуры данных
            analysis["dependencies"] = self._analyze_dependencies(code)
            analysis["data_structures"] = self._analyze_data_structures(code)
            analysis["output_patterns"] = self._analyze_output_patterns(code)

        except SyntaxError as e:
            print(f"Ошибка синтаксиса при анализе кода: {e}")

        return analysis

    def _analyze_function(self, func_node: ast.FunctionDef, code: str) -> Dict:
        """Анализирует отдельную функцию"""
        func_info = {
            "name": func_node.name,
            "args": [arg.arg for arg in func_node.args.args],
            "has_print": (
                "print(" in code[func_node.end_lineno - 1 : func_node.end_lineno + 10]
                if func_node.end_lineno
                else False
            ),
            "is_random": (
                "random" in code[func_node.lineno - 1 : func_node.end_lineno]
                if func_node.end_lineno
                else False
            ),
            "has_loops": any(
                isinstance(node, (ast.For, ast.While)) for node in ast.walk(func_node)
            ),
            "has_conditionals": any(
                isinstance(node, (ast.If, ast.Try)) for node in ast.walk(func_node)
            ),
            "complexity": self._calculate_complexity(func_node),
            "docstring": ast.get_docstring(func_node) or "",
            "line_range": (func_node.lineno, func_node.end_lineno),
        }
        return func_info

    def _analyze_dependencies(self, code: str) -> Dict:
        """Анализирует зависимости в коде"""
        deps = {"imports": [], "external_libs": [], "data_files": []}

        lines = code.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("import "):
                deps["imports"].append(line)
            elif line.startswith("from "):
                deps["imports"].append(line)
            elif "random" in line:
                deps["external_libs"].append("random")
            elif "json" in line or "csv" in line:
                deps["data_files"].append("file_processing")

        return deps

    def _analyze_data_structures(self, code: str) -> Dict:
        """Анализирует структуры данных в коде"""
        structures = {"lists": [], "dicts": [], "sets": [], "tuples": []}

        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ListComp):
                    structures["lists"].append("list_comprehension")
                elif isinstance(node, ast.DictComp):
                    structures["dicts"].append("dict_comprehension")
                elif isinstance(node, ast.SetComp):
                    structures["sets"].append("set_comprehension")
        except:
            pass

        return structures

    def _analyze_output_patterns(self, code: str) -> Dict:
        """Анализирует паттерны вывода в коде"""
        patterns = {"print_functions": [], "output_types": set(), "formatting": []}

        lines = code.split("\n")
        for line in lines:
            if "print(" in line:
                patterns["print_functions"].append(line.strip())
                if ".format(" in line or "%" in line:
                    patterns["formatting"].append("string_formatting")
                if "\\n" in line or "\n" in line:
                    patterns["output_types"].add("multiline")
                else:
                    patterns["output_types"].add("single_line")

        return patterns

    def _calculate_complexity(self, func_node: ast.FunctionDef) -> int:
        """Вычисляет цикломатическую сложность функции"""
        complexity = 1  # базовая сложность

        for node in ast.walk(func_node):
            if isinstance(
                node, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.Assert)
            ):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1

        return complexity

    def get_new_functions(self) -> Set[str]:
        """Возвращает множество новых функций, для которых нужно создать тесты"""
        app_file = self.config.get("app_file", "app.py")

        if not os.path.exists(app_file):
            return set()

        with open(app_file, "r", encoding="utf-8") as f:
            current_code = f.read()

        current_functions = self.extract_functions_from_code(current_code)

        # Считаем файл test_generated пустым по умолчанию
        # Все функции в app.py считаются новыми и требующими тестов
        return current_functions

    def extract_code_from_response(self, text: str) -> str:
        """Извлекает Python-код из ответа модели"""
        lines = text.split("\n")
        cleaned_lines = []
        for line in lines:
            if line.strip() in ("```python", "```"):
                continue
            cleaned_lines.append(line)
        return "\n".join(cleaned_lines).strip()

    def generate_tests_for_functions(self, functions: List[str]) -> str:
        """Генерирует тесты для указанных функций"""
        if not functions:
            return ""

        app_file = self.config.get("app_file", "app.py")

        with open(app_file, "r", encoding="utf-8") as f:
            full_code = f.read()

        # Проверяем, доступен ли API
        api_key = os.getenv("OPENROUTER_API_KEY")
        use_api = api_key and self._check_api_credits()

        if use_api:
            return self._generate_tests_with_api(functions, full_code)
        else:
            print("API недоступен или нет кредитов, используем шаблонную генерацию...")
            return self._generate_tests_template(functions, full_code)

    def _check_api_credits(self) -> bool:
        """Проверяет доступность API кредитов"""
        try:
            # Простая проверка - если API ключ установлен, предполагаем что кредиты есть
            return True
        except:
            return False

    def _generate_tests_with_api(self, functions: List[str], full_code: str) -> str:
        """Генерация тестов через API с использованием анализа кода"""
        functions_str = ", ".join(functions)

        # Сначала анализируем код
        code_analysis = self.analyze_code_structure(full_code)

        # Создаем детальный промпт на основе анализа
        prompt = self._create_enhanced_prompt(functions, full_code, code_analysis)

        api_key = os.getenv("OPENROUTER_API_KEY")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.config.get("settings", {}).get(
                "api_model", "meta-llama/llama-3.3-8b-instruct:free"
            ),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.config.get("settings", {}).get("temperature", 0),
            "max_tokens": self.config.get("settings", {}).get("max_tokens", 2000),
        }

        print("Отправляем запрос в API для генерации тестов...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data
        )

        if response.status_code != 200:
            print(f"Ошибка API: {response.status_code}")
            print(response.text)
            return ""

        result = response.json()
        raw_response = result["choices"][0]["message"]["content"]
        code_only = self.extract_code_from_response(raw_response)
        return code_only

    def _create_enhanced_prompt(
        self, functions: List[str], code: str, analysis: Dict
    ) -> str:
        """Создает улучшенный промпт на основе анализа кода"""
        functions_str = ", ".join(functions)

        # Получаем детальную информацию о функциях
        functions_info = []
        for func_name in functions:
            if func_name in analysis["functions"]:
                func_info = analysis["functions"][func_name]
                info = f"""
                Функция: {func_name}
                - Аргументы: {func_info['args']}
                - Печатает вывод: {'Да' if func_info['has_print'] else 'Нет'}
                - Использует random: {'Да' if func_info['is_random'] else 'Нет'}
                - Сложность: {func_info['complexity']}
                - Циклы: {'Есть' if func_info['has_loops'] else 'Нет'}
                - Условия: {'Есть' if func_info['has_conditionals'] else 'Нет'}
                """
                functions_info.append(info)

        functions_details = "\n".join(functions_info)

        prompt = f"""
        Проанализируй код и создай точные pytest тесты для функций: {functions_str}

        ДЕТАЛЬНЫЙ АНАЛИЗ КОДА:
        {functions_details}

        СТРУКТУРА ПРОЕКТА:
        - Зависимости: {analysis['dependencies']}
        - Структуры данных: {analysis['data_structures']}
        - Паттерны вывода: {analysis['output_patterns']}

        ТРЕБОВАНИЯ К ТЕСТАМ:
        1. Создай ОТДЕЛЬНЫЙ тест для КАЖДОЙ функции
        2. Используй точные имена функций из анализа
        3. Для функций с выводом: захвати stdout и проверь ТОЧНЫЙ текст
        4. Для функций со случайностью: зафиксируй seed=42
        5. Для функций обработки данных: проверь точные значения

        СПЕЦИФИЧЕСКИЕ ИНСТРУКЦИИ:
        - Анализируй каждую функцию индивидуально
        - Создавай реалистичные тестовые данные на основе анализа
        - Проверяй точное форматирование вывода включая пробелы и переносы строк
        - Используй assert для проверки ожидаемых результатов

        ФОРМАТ ТЕСТОВ:
        ```python
        import pytest
        import io
        import sys
        from unittest.mock import patch
        from app import [список_функций]

        def test_имя_функции():
            \"\"\"Описание того, что тестирует функция\"\"\"
            # Тело теста на основе анализа
        ```

        ПОЛНЫЙ КОД ДЛЯ АНАЛИЗА:
        {code}

        Создай тесты для функций: {functions_str}
        """

        return prompt

        api_key = os.getenv("OPENROUTER_API_KEY")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.config.get("settings", {}).get(
                "api_model", "meta-llama/llama-3.1-70b-instruct"
            ),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.config.get("settings", {}).get("temperature", 0),
            "max_tokens": self.config.get("settings", {}).get("max_tokens", 2000),
        }

        print("Отправляем запрос в API для генерации тестов...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data
        )

        if response.status_code != 200:
            print(f"Ошибка API: {response.status_code}")
            print(response.text)
            return ""

        result = response.json()
        raw_response = result["choices"][0]["message"]["content"]
        code_only = self.extract_code_from_response(raw_response)
        return code_only

    def _generate_tests_template(self, functions: List[str], full_code: str) -> str:
        """Шаблонная генерация тестов без API"""
        tests = []
        tests.append("import pytest")
        tests.append("import io")
        tests.append("import sys")
        tests.append("from app import (")
        tests.append("    " + ", ".join(functions))
        tests.append(")")
        tests.append("")

        for func_name in functions:
            test_code = self._generate_single_test_template(func_name, full_code)
            tests.extend(test_code)

        return "\n".join(tests)

    def _generate_single_test_template(
        self, func_name: str, full_code: str
    ) -> List[str]:
        """Генерирует шаблонный тест для одной функции"""
        test_lines = [f"def test_{func_name}():"]

        # Анализируем функцию для определения типа теста
        if self._function_prints_output(func_name, full_code):
            test_lines.extend(
                [
                    '    """Test {func_name} function output"""',
                    "    captured_output = io.StringIO()",
                    "    sys.stdout = captured_output",
                    "",
                    "    try:",
                    f"        {func_name}()",
                    "        sys.stdout = sys.__stdout__",
                    "        # TODO: Replace with actual expected output",
                    '        expected_output = "EXPECTED_OUTPUT_HERE"',
                    "        assert captured_output.getvalue().strip() == expected_output",
                    "    finally:",
                    "        sys.stdout = sys.__stdout__",
                ]
            )
        else:
            test_lines.extend(
                [
                    '    """Test {func_name} function"""',
                    f"        # TODO: Implement test for {func_name}",
                    "        # This function doesn't print output, test its return value or side effects",
                    "        pass",
                ]
            )

        test_lines.append("")
        return test_lines

    def _function_prints_output(self, func_name: str, code: str) -> bool:
        """Определяет, печатает ли функция вывод"""
        # Простая эвристика: если в коде есть print, считаем что функция печатает
        return f"print(" in code and f"def {func_name}(" in code

    def append_tests_to_file(self, new_tests: str):
        """Добавляет новые тесты к существующему файлу тестов"""
        tests_file = self.config.get("tests_file", "test_generated.py")

        # Если файл не существует, создаем его
        if not os.path.exists(tests_file):
            with open(tests_file, "w", encoding="utf-8") as f:
                f.write(new_tests)
            print(f"Создан новый файл тестов: {tests_file}")
            return

        # Читаем существующие тесты
        with open(tests_file, "r", encoding="utf-8") as f:
            existing_content = f.read()

        # Добавляем новые тесты в конец файла
        updated_content = existing_content.rstrip() + "\n\n" + new_tests

        # Проверяем синтаксис
        try:
            compile(updated_content, "<string>", "exec")
            print("Сгенерированный код валиден")
        except SyntaxError as e:
            print(f"Синтаксическая ошибка в сгенерированном коде: {e}")
            print("Сохраняем как есть...")

        with open(tests_file, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print(f"Новые тесты добавлены в {tests_file}")

    def generate_and_append_tests(self) -> bool:
        """Генерирует и добавляет тесты для новых функций с использованием анализа кода"""
        new_functions = list(self.get_new_functions())

        if not new_functions:
            print("Нет новых функций для тестирования")
            return False

        print(f"Найдены новые функции: {', '.join(new_functions)}")

        # Читаем код для анализа
        app_file = self.config.get("app_file", "app.py")
        with open(app_file, "r", encoding="utf-8") as f:
            full_code = f.read()

        # Выполняем глубокий анализ кода
        print("Выполняем анализ структуры кода...")
        code_analysis = self.analyze_code_structure(full_code)

        # Выводим результаты анализа
        self._print_analysis_summary(code_analysis, new_functions)

        # Генерируем тесты для новых функций с использованием анализа
        new_tests = self.generate_tests_for_functions(new_functions)

        if not new_tests:
            print("Не удалось сгенерировать тесты")
            return False

        # Добавляем тесты в файл
        self.append_tests_to_file(new_tests)

        # Обновляем хэш файла
        self.tracker.update_hash(self.config.get("app_file", "app.py"))

        # Добавляем информацию о новых тестах в историю
        for func in new_functions:
            self.tracker.add_test_to_history(f"test_{func}", "generated", [func])

        return True

    def _print_analysis_summary(self, analysis: Dict, functions: List[str]):
        """Выводит краткое резюме анализа кода"""
        print("\n=== РЕЗУЛЬТАТЫ АНАЛИЗА КОДА ===")

        # Анализ функций
        functions_info = analysis.get("functions", {})
        for func_name in functions:
            if func_name in functions_info:
                func_info = functions_info[func_name]
                print(f"\nФункция: {func_name}")
                print(f"  Сложность: {func_info['complexity']}")
                print(f"  Печатает: {'Да' if func_info['has_print'] else 'Нет'}")
                print(f"  Random: {'Да' if func_info['is_random'] else 'Нет'}")
                print(f"  Циклы: {'Да' if func_info['has_loops'] else 'Нет'}")

        # Зависимости
        deps = analysis.get("dependencies", {})
        if deps.get("external_libs"):
            print(f"\nВнешние библиотеки: {', '.join(deps['external_libs'])}")

        print("Анализ завершен, генерируем адаптированные тесты...\n")

    def run_full_cycle(self) -> bool:
        """Выполняет полный цикл: проверка, очистка, генерация"""
        print("=== НАЧАЛО ЦИКЛА ГЕНЕРАЦИИ ТЕСТОВ ===")

        # Всегда считаем файл измененным и генерируем тесты для всех функций
        print("Анализируем функции в app.py и генерируем тесты...")

        # Выводим отчет о валидации
        self.validator.print_validation_report()

        # Удаляем устаревшие тесты только если есть реальные устаревшие функции
        obsolete_tests = self.validator.get_obsolete_tests()
        if obsolete_tests:
            print(f"Найдены устаревшие тесты: {len(obsolete_tests)}")
            removed_count = self.validator.remove_obsolete_tests()
            if removed_count > 0:
                print(f"Удалено устаревших тестов: {removed_count}")
        else:
            print("Устаревших тестов не найдено")

        # Генерируем новые тесты для всех функций в app.py
        success = self.generate_and_append_tests()

        if success:
            print("Цикл генерации тестов завершен успешно")
        else:
            print("Цикл генерации тестов завершен без изменений в тестах")

        return success


def main():
    """Основная функция для тестирования"""
    generator = SmartTestGenerator()
    generator.run_full_cycle()


if __name__ == "__main__":
    main()
