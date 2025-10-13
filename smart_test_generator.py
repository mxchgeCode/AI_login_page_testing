import ast
import json
import os
import requests
from typing import Dict, List, Set
from code_tracker import CodeTracker
from test_validator import TestValidator


class SmartTestGenerator:
    """Умный генератор тестов, который генерирует тесты только для новых функций"""

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

        # Создаем промпт для генерации тестов только для новых функций
        functions_str = ", ".join(functions)
        prompt = f"""
        You are a Python developer. Generate pytest unit tests for the following functions: {functions_str}.

        The code resides in the module named 'app'. Write ONLY Python code, no explanations or markdown.

        CRITICAL TESTING REQUIREMENTS:
        - Use pytest fixtures (capsys, tmp_path, etc.) instead of unittest.mock.patch where possible
        - Use assert statements directly, not self.assertEqual()
        - Use descriptive test function names starting with 'test_'
        - For output capture, prefer capsys fixture over patch('sys.stdout')
        - Use pytest.raises() for exception testing instead of self.assertRaises()

        SPECIFIC TESTING PATTERNS:
        - For functions that print output: use capsys fixture and check captured.out
        - For functions that return values: use direct assert statements
        - For functions with randomness: mock random values or use pytest fixtures
        - For functions with side effects: capture and verify the effects

        CODE ANALYSIS:
        - Analyze the function implementation carefully
        - Understand what the function does and what it outputs
        - Create tests that verify the CORRECT behavior based on actual function logic
        - Handle edge cases and error conditions

        IMPORTANT: Generate tests that match the ACTUAL behavior of the functions, not hypothetical behavior.

        Tests should import necessary functions from 'app' module and use mocking only when necessary.

        Here is the full code context:

        {full_code}

        Generate tests only for these specific functions: {functions_str}
        """

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Ошибка: OPENROUTER_API_KEY не установлен")
            return ""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.config.get("settings", {}).get(
                "api_model", "meta-llama/llama-3.1-8b-instruct:free"
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
        """Генерирует и добавляет тесты для новых функций"""
        new_functions = list(self.get_new_functions())

        if not new_functions:
            print("Нет новых функций для тестирования")
            return False

        print(f"Найдены новые функции: {', '.join(new_functions)}")

        # Генерируем тесты для новых функций
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
