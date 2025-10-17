#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для автоматического получения реального вывода функций
"""
import ast
import importlib.util
import io
import sys
from typing import Dict, Any, Callable


class FunctionOutputCapture:
    """Класс для захвата вывода функций"""

    def __init__(self, app_file: str = "app.py"):
        self.app_file = app_file
        self.function_outputs = {}

    def extract_functions_from_code(self, code: str) -> list:
        """Извлекает названия функций из кода"""
        functions = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
        except SyntaxError:
            pass
        return functions

    def capture_function_output(self, func_name: str) -> str:
        """Захватывает вывод конкретной функции"""
        try:
            # Загружаем модуль динамически
            spec = importlib.util.spec_from_file_location("app", self.app_file)
            app_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(app_module)

            # Получаем функцию
            if hasattr(app_module, func_name):
                func = getattr(app_module, func_name)

                # Захватываем вывод
                captured_output = io.StringIO()
                old_stdout = sys.stdout
                sys.stdout = captured_output

                try:
                    # Вызываем функцию
                    func()
                    output = captured_output.getvalue().strip()
                    return output
                finally:
                    sys.stdout = old_stdout
            else:
                return f"Function {func_name} not found"

        except Exception as e:
            return f"Error capturing output for {func_name}: {e}"

    def capture_all_functions_output(self) -> Dict[str, str]:
        """Захватывает вывод всех функций в файле"""
        with open(self.app_file, 'r', encoding='utf-8') as f:
            code = f.read()

        functions = self.extract_functions_from_code(code)
        outputs = {}

        for func_name in functions:
            output = self.capture_function_output(func_name)
            outputs[func_name] = output

        return outputs

    def generate_test_from_output(self, func_name: str, output: str) -> str:
        """Генерирует тест на основе захваченного вывода"""
        test_code = f'''def test_{func_name}():
    """Test {func_name} function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        {func_name}()
        sys.stdout = sys.__stdout__
        expected_output = """{output}"""
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__

'''
        return test_code


def main():
    """Основная функция для захвата выводов"""
    capturer = FunctionOutputCapture()

    print("Захватываем вывод всех функций...")
    outputs = capturer.capture_all_functions_output()

    print("\n=== РЕЗУЛЬТАТЫ ЗАХВАТА ===")
    for func_name, output in outputs.items():
        print(f"\n{func_name}():")
        print(repr(output))

    # Генерируем тесты
    print("\n=== ГЕНЕРАЦИЯ ТЕСТОВ ===")
    test_code = '''import io
import sys
from app import *

'''

    for func_name, output in outputs.items():
        if output and "Error" not in output and "not found" not in output:
            test_code += capturer.generate_test_from_output(func_name, output)

    # Сохраняем тесты
    with open("test_generated.py", "w", encoding="utf-8") as f:
        f.write(test_code)

    print("Тесты сохранены в test_generated.py")


if __name__ == "__main__":
    main()