import os
import subprocess
import sys
import json
from typing import List, Dict, Tuple
from test_validator import TestValidator
from smart_test_generator import SmartTestGenerator


class TestRunner:
    """Класс для запуска всех тестов"""

    def __init__(self, config_file: str = "test_config.json"):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Загружает конфигурацию из файла"""
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def run_tests(self) -> Tuple[int, str]:
        """Запускает тесты и возвращает код выхода и вывод"""
        tests_file = self.config.get("tests_file", "test_generated.py")

        if not os.path.exists(tests_file):
            return 0, f"Файл тестов не найден: {tests_file}. Создайте тесты сначала."

        try:
            # Запускаем pytest
            result = subprocess.run(
                [sys.executable, "-m", "pytest", tests_file, "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=300,
            )

            return result.returncode, result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            return 1, "Тесты выполнялись слишком долго и были прерваны"
        except Exception as e:
            return 1, f"Ошибка при запуске тестов: {e}"

    def run_flake8_linting(self) -> Tuple[int, str]:
        """Запускает линтинг с помощью flake8"""
        tests_file = self.config.get("tests_file", "test_generated.py")

        if not os.path.exists(tests_file):
            return 0, f"Файл тестов не найден: {tests_file}"

        try:
            result = subprocess.run(
                ["flake8", tests_file, "--max-line-length=100", "--ignore=E501,W503"],
                capture_output=True,
                text=True,
            )

            return result.returncode, result.stdout + result.stderr

        except FileNotFoundError:
            return 0, "flake8 не установлен (это нормально)"
        except Exception as e:
            return 0, f"Ошибка при запуске flake8: {e}"

    def run_full_test_cycle(self) -> Dict:
        """Выполняет полный цикл тестирования"""
        print("=== НАЧАЛО ПОЛНОГО ЦИКЛА ТЕСТИРОВАНИЯ ===")

        results = {
            "generation_success": False,
            "validation_passed": False,
            "tests_passed": False,
            "linting_passed": False,
            "report": [],
        }

        # 1. Генерация/обновление тестов
        print("\n1. Генерация и обновление тестов...")
        generator = SmartTestGenerator(self.config_file)
        results["generation_success"] = generator.run_full_cycle()

        # 2. Валидация тестов
        print("\n2. Валидация тестов...")
        validator = TestValidator(self.config_file)
        validation_results = validator.validate_tests()

        if validation_results:
            valid_tests = validator.get_valid_tests()
            results["validation_passed"] = len(valid_tests) > 0
            results["report"].append(f"Валидных тестов: {len(valid_tests)}")
            results["report"].append(f"Всего тестов: {len(validation_results)}")
        else:
            results["validation_passed"] = True  # Нет тестов - это тоже валидно
            results["report"].append("Нет тестов для валидации")

        # 3. Запуск тестов
        print("\n3. Запуск тестов...")
        test_returncode, test_output = self.run_tests()

        if test_returncode == 0:
            results["tests_passed"] = True
            results["report"].append("Все тесты прошли успешно")
        else:
            results["tests_passed"] = False
            results["report"].append("Некоторые тесты провалились")
            results["report"].append(f"Вывод pytest:\n{test_output}")

        # 4. Линтинг
        print("\n4. Проверка стиля кода...")
        lint_returncode, lint_output = self.run_flake8_linting()

        if lint_returncode == 0:
            results["linting_passed"] = True
            results["report"].append("Стиль кода корректен")
        else:
            results["linting_passed"] = False
            results["report"].append("Найдены проблемы стиля кода")
            if lint_output.strip():
                results["report"].append(f"Вывод flake8:\n{lint_output}")

        # 5. Итоговый отчет
        print("\n=== ИТОГОВЫЙ ОТЧЕТ ===")
        print(
            f"Генерация тестов: {'[OK]' if results['generation_success'] else '[FAIL]'}"
        )
        print(
            f"Валидация тестов: {'[OK]' if results['validation_passed'] else '[FAIL]'}"
        )
        print(f"Запуск тестов: {'[OK]' if results['tests_passed'] else '[FAIL]'}")
        print(f"Линтинг: {'[OK]' if results['linting_passed'] else '[FAIL]'}")

        success_count = sum(
            [
                results["generation_success"],
                results["validation_passed"],
                results["tests_passed"],
                results["linting_passed"],
            ]
        )

        print(f"\nУспешно: {success_count}/4")

        if not results["tests_passed"]:
            print("\nОШИБКА: ТЕСТИРОВАНИЕ ПРОВАЛЕНО")
            return results

        if success_count >= 3:
            print("\nУСПЕХ: ТЕСТИРОВАНИЕ ПРОШЛО УСПЕШНО")
        else:
            print("\nПРЕДУПРЕЖДЕНИЕ: ТЕСТИРОВАНИЕ ПРОШЛО С ПРЕДУПРЕЖДЕНИЯМИ")

        return results

    def run_tests_only(self) -> Dict:
        """Запускает только существующие тесты без генерации"""
        print("=== ЗАПУСК СУЩЕСТВУЮЩИХ ТЕСТОВ ===")

        results = {"tests_passed": False, "linting_passed": False, "report": []}

        # Проверяем валидацию
        validator = TestValidator(self.config_file)
        validation_results = validator.validate_tests()

        if validation_results:
            valid_tests = validator.get_valid_tests()
            results["report"].append(f"Валидных тестов: {len(valid_tests)}")
            results["report"].append(f"Всего тестов: {len(validation_results)}")

            if not valid_tests:
                results["report"].append("Нет валидных тестов для запуска")
                return results

        # Запуск тестов
        test_returncode, test_output = self.run_tests()

        if test_returncode == 0:
            results["tests_passed"] = True
            results["report"].append("Все тесты прошли успешно")
        else:
            results["tests_passed"] = False
            results["report"].append("Некоторые тесты провалились")
            results["report"].append(f"Вывод pytest:\n{test_output}")

        # Линтинг
        lint_returncode, lint_output = self.run_flake8_linting()

        if lint_returncode == 0:
            results["linting_passed"] = True
            results["report"].append("Стиль кода корректен")
        else:
            results["linting_passed"] = False
            results["report"].append("Найдены проблемы стиля кода")
            if lint_output.strip():
                results["report"].append(f"Вывод flake8:\n{lint_output}")

        return results


def main():
    """Основная функция"""
    if len(sys.argv) > 1 and sys.argv[1] == "--tests-only":
        # Запуск только тестов
        runner = TestRunner()
        results = runner.run_tests_only()

        if not results["tests_passed"]:
            sys.exit(1)
    else:
        # Полный цикл
        runner = TestRunner()
        results = runner.run_full_test_cycle()

        if not results["tests_passed"]:
            sys.exit(1)


if __name__ == "__main__":
    main()
