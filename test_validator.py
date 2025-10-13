import ast
import json
import os
from typing import Dict, List, Set
from code_tracker import CodeTracker


class TestValidator:
    """Класс для проверки актуальности существующих тестов"""

    def __init__(self, config_file: str = "test_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.tracker = CodeTracker(config_file)

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

    def extract_functions_from_file(self, file_path: str) -> Set[str]:
        """Извлекает названия функций из файла"""
        if not os.path.exists(file_path):
            return set()

        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        return self.extract_functions_from_code(code)

    def extract_test_functions_from_file(self, file_path: str) -> Dict[str, List[str]]:
        """Извлекает тестовые функции и их покрываемые функции из файла тестов"""
        if not os.path.exists(file_path):
            return {}

        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        test_functions = {}

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                    covered_functions = self._extract_covered_functions_from_test(node)
                    test_functions[node.name] = covered_functions

        except SyntaxError as e:
            print(f"Ошибка синтаксиса при парсинге тестов: {e}")

        return test_functions

    def _extract_covered_functions_from_test(
        self, test_node: ast.FunctionDef
    ) -> List[str]:
        """Извлекает названия функций, покрываемых тестом"""
        covered_functions = []

        # Анализируем вызовы функций внутри тела теста
        for node in ast.walk(test_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    # Прямой вызов функции
                    func_name = node.func.id
                    # Проверяем, что это функция из app модуля (не встроенная функция Python)
                    if func_name in ['solve_task_one', 'solve_task_two', 'solve_task_three', 'solve_task_four', 'solve_ternary_operator']:
                        covered_functions.append(func_name)

        return list(set(covered_functions))  # Убираем дубликаты

    def validate_tests(self) -> Dict[str, Dict[str, any]]:
        """Проверяет актуальность всех тестов"""
        app_file = self.config.get("app_file", "app.py")
        tests_file = self.config.get("tests_file", "test_generated.py")

        if not os.path.exists(app_file):
            return {}

        if not os.path.exists(tests_file):
            print(f"Файл тестов не найден: {tests_file}")
            return {}

        # Получаем функции из основного кода
        app_functions = self.extract_functions_from_file(app_file)

        # Получаем тестовые функции и их покрытие
        test_functions = self.extract_test_functions_from_file(tests_file)

        if not test_functions:
            print("В файле тестов не найдены тестовые функции")
            return {}

        validation_results = {}

        for test_name, covered_functions in test_functions.items():
            # Проверяем, какие функции из покрываемых тестом все еще существуют
            existing_functions = [
                func for func in covered_functions if func in app_functions
            ]
            missing_functions = [
                func for func in covered_functions if func not in app_functions
            ]

            is_valid = len(missing_functions) == 0

            validation_results[test_name] = {
                "is_valid": is_valid,
                "covered_functions": covered_functions,
                "existing_functions": existing_functions,
                "missing_functions": missing_functions,
                "coverage_percentage": (
                    len(existing_functions) / len(covered_functions) * 100
                    if covered_functions
                    else 0
                ),
            }

        return validation_results

    def get_obsolete_tests(self) -> List[str]:
        """Возвращает список устаревших тестов"""
        validation_results = self.validate_tests()
        return [
            test_name
            for test_name, result in validation_results.items()
            if not result["is_valid"]
        ]

    def get_valid_tests(self) -> List[str]:
        """Возвращает список актуальных тестов"""
        validation_results = self.validate_tests()
        return [
            test_name
            for test_name, result in validation_results.items()
            if result["is_valid"]
        ]

    def print_validation_report(self):
        """Выводит отчет о валидации тестов"""
        validation_results = self.validate_tests()

        if not validation_results:
            print("Нет тестов для проверки или файлы не найдены")
            return

        print("\n=== ОТЧЕТ О ВАЛИДАЦИИ ТЕСТОВ ===")
        print(f"Всего тестов: {len(validation_results)}")

        valid_tests = self.get_valid_tests()
        obsolete_tests = self.get_obsolete_tests()

        print(f"Актуальных тестов: {len(valid_tests)}")
        print(f"Устаревших тестов: {len(obsolete_tests)}")

        if obsolete_tests:
            print(f"\nУстаревшие тесты (нужно обновить или удалить):")
            for test_name in obsolete_tests:
                result = validation_results[test_name]
                missing = ", ".join(result["missing_functions"])
                print(f"  - {test_name}: отсутствуют функции - {missing}")

        if valid_tests:
            print(f"\nАктуальные тесты:")
            for test_name in valid_tests:
                result = validation_results[test_name]
                coverage = result["coverage_percentage"]
                print(f"  - {test_name}: покрытие {coverage:.1f}%")

    def remove_obsolete_tests(self) -> int:
        """Удаляет устаревшие тесты из файла"""
        tests_file = self.config.get("tests_file", "test_generated.py")

        if not os.path.exists(tests_file):
            return 0

        # Читаем текущие тесты
        with open(tests_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Получаем устаревшие тесты
        obsolete_tests = self.get_obsolete_tests()

        if not obsolete_tests:
            print("Нет устаревших тестов для удаления")
            return 0

        # Создаем новое содержимое без устаревших тестов
        lines = content.split("\n")
        new_lines = []
        current_test = None
        test_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]

            # Проверяем, начинается ли новая функция
            if line.strip().startswith("def ") and "(" in line:
                # Если у нас был предыдущий тест, сохраняем или пропускаем его
                if current_test and test_lines:
                    if current_test not in obsolete_tests:
                        new_lines.extend(test_lines)
                    else:
                        print(f"Удален устаревший тест: {current_test}")

                # Начинаем новый тест
                current_test = line.strip().split("(")[0].replace("def ", "")
                test_lines = [line]
            else:
                if current_test:
                    test_lines.append(line)

            i += 1

        # Обрабатываем последний тест
        if current_test and test_lines:
            if current_test not in obsolete_tests:
                new_lines.extend(test_lines)
            else:
                print(f"Удален устаревший тест: {current_test}")

        # Если не было тестов, копируем все содержимое
        if not new_lines:
            new_lines = lines

        # Записываем обновленный файл
        with open(tests_file, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))

        return len(obsolete_tests)


def main():
    """Основная функция для тестирования"""
    validator = TestValidator()
    validator.print_validation_report()

    print(f"\nУдаляем устаревшие тесты...")
    removed_count = validator.remove_obsolete_tests()
    print(f"Удалено тестов: {removed_count}")


if __name__ == "__main__":
    main()
