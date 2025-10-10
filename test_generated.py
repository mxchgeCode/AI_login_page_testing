import pytest
import io
import sys
from unittest.mock import patch
from app import solve_task_one, solve_task_two


# === ЮНИТ-ТЕСТЫ ДЛЯ ФУНКЦИЙ ===

def test_solve_task_one_books_total():
    """Тест функции solve_task_one для правильного подсчета прибыли Books"""
    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        solve_task_one()

    output = captured_output.getvalue()

    # Проверяем, что Books посчитаны правильно: 1343 + 1166 + 848 + 815 + 1218 + 1003 + 920 + 656 = 7969
    assert "Books: $7969" in output


def test_solve_task_one_courses_total():
    """Тест функции solve_task_one для правильного подсчета прибыли Courses"""
    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        solve_task_one()

    output = captured_output.getvalue()

    # Проверяем, что Courses посчитаны правильно: 966 + 1061 + 964 = 2991
    assert "Courses: $2991" in output


def test_solve_task_one_merch_total():
    """Тест функции solve_task_one для правильного подсчета прибыли Merch"""
    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        solve_task_one()

    output = captured_output.getvalue()

    # Проверяем, что Merch посчитаны правильно: 616 + 1145 + 642 + 951 + 729 = 4083
    assert "Merch: $4083" in output


def test_solve_task_one_tutorials_total():
    """Тест функции solve_task_one для правильного подсчета прибыли Tutorials"""
    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        solve_task_one()

    output = captured_output.getvalue()

    # Проверяем, что Tutorials посчитаны правильно: 832 + 1041 + 880 + 977 = 3730
    assert "Tutorials: $3730" in output


def test_solve_task_two_departments_count():
    """Тест функции solve_task_two для правильного подсчета сотрудников по отделам"""
    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        solve_task_two()

    output = captured_output.getvalue()

    # Проверяем правильность подсчета сотрудников по отделам
    assert "Accounting: 17" in output
    assert "Developing: 7" in output
    assert "Marketing: 13" in output
    assert "Sales: 13" in output


def test_solve_task_one_output_order():
    """Тест функции solve_task_one для правильного порядка вывода"""
    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        solve_task_one()

    output = captured_output.getvalue()

    # Проверяем, что вывод отсортирован по алфавиту
    lines = [line.strip() for line in output.split('\n') if line.strip() and '$' in line]
    assert lines[0] == "Books: $7969"
    assert lines[1] == "Courses: $2991"
    assert lines[2] == "Merch: $4083"
    assert lines[3] == "Tutorials: $3730"


def test_solve_task_two_output_order():
    """Тест функции solve_task_two для правильного порядка вывода отделов"""
    captured_output = io.StringIO()
    with patch('sys.stdout', captured_output):
        solve_task_two()

    output = captured_output.getvalue()

    # Проверяем, что отделы отсортированы по алфавиту
    lines = [line.strip() for line in output.split('\n') if line.strip() and ':' in line]
    assert lines[0] == "Accounting: 17"
    assert lines[1] == "Developing: 7"
    assert lines[2] == "Marketing: 13"
    assert lines[3] == "Sales: 13"


# === ПРИМЕЧАНИЕ ===
# Функции solve_task_one() и solve_task_two() полностью покрыты юнит-тестами выше
# Тесты проверяют правильность подсчета данных и порядок вывода результатов


# Тесты будут генерироваться автоматически при изменении app.py
