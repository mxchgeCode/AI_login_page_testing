#!/usr/bin/env python3
"""
Скрипт для запуска тестов с измерением покрытия кода
"""

import subprocess
import sys
import os


def run_tests_with_coverage():
    """Запускает тесты с coverage и генерирует отчеты"""
    print("Запуск тестов с измерением покрытия кода")
    print("=" * 60)

    # Проверяем, установлен ли coverage
    try:
        import coverage
    except ImportError:
        print("Coverage не установлен. Установите: pip install coverage pytest-cov")
        return False

    # Запускаем тесты с coverage
    print("Запускаем тесты с coverage...")
    cmd = [
        "coverage", "run",
        "-m", "pytest",
        "test_generated.py",
        "-v",
        "--cov=app",
        "--cov-report=term",
        "--cov-report=html",
        "--cov-report=xml"
    ]

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)

        if result.returncode == 0:
            print("Тесты прошли успешно!")

            # Генерируем дополнительные отчеты
            print("Генерируем отчеты покрытия...")

            # HTML отчет
            html_result = subprocess.run(["coverage", "html", "-d", "coverage_html"], capture_output=True, text=True)

            # XML отчет для CI/CD
            xml_result = subprocess.run(["coverage", "xml", "-o", "coverage.xml"], capture_output=True, text=True)

            # JSON отчет
            json_result = subprocess.run(["coverage", "json", "-o", "coverage.json"], capture_output=True, text=True)

            # Подробный текстовый отчет
            print("\nПодробный отчет покрытия:")
            report_result = subprocess.run(["coverage", "report", "-m"], capture_output=True, text=True)

            # Проверяем, были ли ошибки
            if html_result.returncode == 0 and xml_result.returncode == 0:
                print("\nОтчеты сохранены:")
                print("   coverage_html/ - HTML отчет (откройте index.html в браузере)")
                print("   coverage.xml - XML отчет для CI/CD")
                print("   coverage.json - JSON отчет")
                print("   .coverage - данные покрытия")
            else:
                print("\nПредупреждение: Некоторые отчеты не удалось сгенерировать")
                if html_result.returncode != 0:
                    print(f"   HTML отчет: {html_result.stderr}")
                if xml_result.returncode != 0:
                    print(f"   XML отчет: {xml_result.stderr}")

            return True
        else:
            print("Некоторые тесты провалились")
            return False

    except Exception as e:
        print(f"Ошибка при запуске тестов: {e}")
        return False


def show_coverage_summary():
    """Показывает краткую информацию о покрытии"""
    if not os.path.exists(".coverage"):
        print("Файл покрытия не найден. Запустите тесты сначала.")
        return

    try:
        # Читаем последний отчет
        if os.path.exists("coverage.txt"):
            print("Последний отчет покрытия:")
            with open("coverage.txt", "r") as f:
                content = f.read()
                # Показываем только последние строки с итогами
                lines = content.split("\n")
                for line in reversed(lines):
                    if line.strip() and ("TOTAL" in line or "coverage" in line.lower()):
                        print(f"   {line}")
                        break
        else:
            print("Отчет покрытия не найден")
    except Exception as e:
        print(f"Ошибка при чтении отчета: {e}")


def main():
    """Основная функция"""
    if len(sys.argv) > 1 and sys.argv[1] == "--summary":
        show_coverage_summary()
    else:
        success = run_tests_with_coverage()
        if success:
            show_coverage_summary()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()