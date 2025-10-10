#!/usr/bin/env python3
import io
import sys
from unittest.mock import patch
from app import solve_task_one, solve_task_two

def test_solve_task_one_books_total():
    """Тест функции solve_task_one для правильного подсчета прибыли Books"""
    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        solve_task_one()

    output = captured_output.getvalue()

    # Проверяем, что Books посчитаны правильно: 1343 + 1166 + 848 + 815 + 1218 + 1003 + 920 + 656 = 7969
    if "Books: $7969" in output:
        print("✓ test_solve_task_one_books_total passed")
        return True
    else:
        print("✗ test_solve_task_one_books_total failed")
        print(f"Expected 'Books: $7969' in output, got: {output}")
        return False

def test_solve_task_one_courses_total():
    """Тест функции solve_task_one для правильного подсчета прибыли Courses"""
    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        solve_task_one()

    output = captured_output.getvalue()

    # Проверяем, что Courses посчитаны правильно: 966 + 1061 + 964 = 2991
    if "Courses: $2991" in output:
        print("✓ test_solve_task_one_courses_total passed")
        return True
    else:
        print("✗ test_solve_task_one_courses_total failed")
        print(f"Expected 'Courses: $2991' in output, got: {output}")
        return False

def test_solve_task_two_departments_count():
    """Тест функции solve_task_two для правильного подсчета сотрудников по отделам"""
    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        solve_task_two()

    output = captured_output.getvalue()

    # Проверяем правильность подсчета сотрудников по отделам
    if "Accounting: 17" in output and "Developing: 7" in output and "Marketing: 13" in output and "Sales: 13" in output:
        print("✓ test_solve_task_two_departments_count passed")
        return True
    else:
        print("✗ test_solve_task_two_departments_count failed")
        print(f"Expected all department counts in output, got: {output}")
        return False

def run_all_tests():
    """Запуск всех тестов"""
    print("Запуск тестов...")
    tests = [
        test_solve_task_one_books_total,
        test_solve_task_one_courses_total,
        test_solve_task_two_departments_count,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print(f"\nРезультаты: {passed}/{total} тестов прошли")
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)