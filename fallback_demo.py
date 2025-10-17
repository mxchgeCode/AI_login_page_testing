#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрация работы fallback режима генерации тестов без API
"""

def demo_fallback_generation():
    """Показывает как работает генерация тестов без API"""

    # Шаг 1: Проверка доступности API
    print("Шаг 1: Проверка API...")
    import os
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"API ключ установлен: {api_key is not None}")

    # Шаг 2: Определение режима работы
    if api_key:
        print("Шаг 2: Используем API режим")
        mode = "api"
    else:
        print("Шаг 2: API недоступен, переходим в режим fallback")
        mode = "fallback"

    # Шаг 3: Анализ кода для определения функций
    print("Шаг 3: Анализируем функции в коде...")
    with open("app.py", "r", encoding="utf-8") as f:
        code = f.read()

    # Извлекаем функции (упрощенная логика)
    functions = []
    lines = code.split("\n")
    for line in lines:
        if line.strip().startswith("def ") and "(" in line:
            func_name = line.strip().split("(")[0].replace("def ", "")
            functions.append(func_name)

    print(f"Найденные функции: {functions}")

    # Шаг 4: Генерация шаблонных тестов
    print("Шаг 4: Генерация шаблонных тестов...")

    tests = []
    tests.append("import pytest")
    tests.append("import io")
    tests.append("import sys")
    tests.append("from app import (")
    tests.append("    " + ", ".join(functions))
    tests.append(")")
    tests.append("")

    for func_name in functions:
        # Определяем тип функции
        if "print(" in code and f"def {func_name}(" in code:
            test_type = "prints_output"
        else:
            test_type = "other"

        # Генерируем тест
        if test_type == "prints_output":
            tests.extend([
                f"def test_{func_name}():",
                f'    """Test {func_name} function output"""',
                "    captured_output = io.StringIO()",
                "    sys.stdout = captured_output",
                "",
                "    try:",
                f"        {func_name}()",
                "        sys.stdout = sys.__stdout__",
                "        # TODO: Замените на реальный ожидаемый вывод",
                '        expected_output = "EXPECTED_OUTPUT_HERE"',
                '        assert captured_output.getvalue().strip() == expected_output',
                "    finally:",
                "        sys.stdout = sys.__stdout__",
                ""
            ])
        else:
            tests.extend([
                f"def test_{func_name}():",
                f'    """Test {func_name} function"""',
                f"        # TODO: Реализуйте тест для {func_name}",
                "        # Эта функция не печатает вывод, тестируйте возвращаемое значение",
                "        pass",
                ""
            ])

    # Шаг 5: Сохранение тестов
    test_code = "\n".join(tests)
    with open("test_fallback_demo.py", "w", encoding="utf-8") as f:
        f.write(test_code)

    print("Шаг 5: Тесты сохранены в test_fallback_demo.py")
    print("\n=== СГЕНЕРИРОВАННЫЕ ТЕСТЫ ===")
    print(test_code)

    return test_code

if __name__ == "__main__":
    demo_fallback_generation()