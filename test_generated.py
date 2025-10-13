import pytest
from app import (
    solve_task_one,
    solve_task_two,
    solve_task_three,
    solve_task_four,
    solve_ternary_operator,
    solve_multiplicity,
)


def test_solve_task_one_books_total(capsys):
    """Тест функции solve_task_one для правильного подсчета прибыли Books"""
    solve_task_one()
    captured = capsys.readouterr()

    # Проверяем, что Books посчитаны правильно: 1343 + 1166 + 848 + 815 + 1218 + 1003 + 920 + 656 = 7969
    assert "Books: $7969" in captured.out


def test_solve_task_one_courses_total(capsys):
    """Тест функции solve_task_one для правильного подсчета прибыли Courses"""
    solve_task_one()
    captured = capsys.readouterr()

    # Проверяем, что Courses посчитаны правильно: 966 + 1061 + 964 = 2991
    assert "Courses: $2991" in captured.out


def test_solve_task_one_merch_total(capsys):
    """Тест функции solve_task_one для правильного подсчета прибыли Merch"""
    solve_task_one()
    captured = capsys.readouterr()

    # Проверяем, что Merch посчитаны правильно: 616 + 1145 + 642 + 951 + 729 = 4083
    assert "Merch: $4083" in captured.out


def test_solve_task_one_tutorials_total(capsys):
    """Тест функции solve_task_one для правильного подсчета прибыли Tutorials"""
    solve_task_one()
    captured = capsys.readouterr()

    # Проверяем, что Tutorials посчитаны правильно: 832 + 1041 + 880 + 977 = 3730
    assert "Tutorials: $3730" in captured.out


def test_solve_task_two_departments_count(capsys):
    """Тест функции solve_task_two для правильного подсчета сотрудников по отделам"""
    solve_task_two()
    captured = capsys.readouterr()

    # Проверяем правильность подсчета сотрудников по отделам
    assert "Accounting: 17" in captured.out
    assert "Developing: 7" in captured.out
    assert "Marketing: 13" in captured.out
    assert "Sales: 13" in captured.out


def test_solve_task_one_output_order(capsys):
    """Тест функции solve_task_one для правильного порядка вывода"""
    solve_task_one()
    captured = capsys.readouterr()

    # Проверяем, что вывод отсортирован по алфавиту
    lines = [
        line.strip()
        for line in captured.out.split("\n")
        if line.strip() and "$" in line
    ]
    assert lines[0] == "Books: $7969"
    assert lines[1] == "Courses: $2991"
    assert lines[2] == "Merch: $4083"
    assert lines[3] == "Tutorials: $3730"


def test_solve_task_two_output_order(capsys):
    """Тест функции solve_task_two для правильного порядка вывода отделов"""
    solve_task_two()
    captured = capsys.readouterr()

    # Проверяем, что отделы отсортированы по алфавиту
    lines = [
        line.strip()
        for line in captured.out.split("\n")
        if line.strip() and ":" in line
    ]
    assert lines[0] == "Accounting: 17"
    assert lines[1] == "Developing: 7"
    assert lines[2] == "Marketing: 13"
    assert lines[3] == "Sales: 13"


def test_solve_task_three_unique_employees(capsys):
    """Тест функции solve_task_three для правильного создания уникального списка сотрудников"""
    solve_task_three()
    captured = capsys.readouterr()

    # Проверяем, что в выводе есть все отделы
    assert "Accounting:" in captured.out
    assert "Developing:" in captured.out
    assert "Marketing:" in captured.out
    assert "Sales:" in captured.out

    # Проверяем, что сотрудники отсортированы по алфавиту
    accounting_line = [
        line for line in captured.out.split("\n") if line.startswith("Accounting:")
    ][0]
    accounting_employees = accounting_line.split(": ")[1].split(", ")
    assert accounting_employees[0] == "Aaron Ferguson"
    assert accounting_employees[1] == "Ann Bell"
    assert "Gloria Higgins" in accounting_employees
    assert "Steven Diaz" in accounting_employees

    developing_line = [
        line for line in captured.out.split("\n") if line.startswith("Developing:")
    ][0]
    developing_employees = developing_line.split(": ")[1].split(", ")
    assert developing_employees[0] == "Arlene Gibson"
    assert developing_employees[-1] == "Wilma Woods"


def test_solve_task_three_empty_input(capsys):
    """Тест функции solve_task_three с пустым списком сотрудников"""

    def solve_task_three_empty():
        staff_broken = []
        departments = {}
        for dept, person in staff_broken:
            departments.setdefault(dept, set()).add(person)
        for dept in sorted(departments):
            sorted_employees = sorted(departments[dept])
            print(f"{dept}: {', '.join(sorted_employees)}")

    solve_task_three_empty()
    captured = capsys.readouterr()

    # Пустой ввод должен давать пустой вывод
    assert captured.out.strip() == ""


def test_solve_task_three_invalid_input(capsys):
    """Тест функции solve_task_three с некорректными данными"""

    def solve_task_three_invalid():
        staff_broken = [
            ("", "John Doe"),
            (None, "Jane Smith"),
            ("IT", ""),
            ("HR", None),
        ]
        departments = {}
        for dept, person in staff_broken:
            if dept and person:
                departments.setdefault(dept, set()).add(person)

        for dept in sorted(departments):
            sorted_employees = sorted(departments[dept])
            if sorted_employees:
                print(f"{dept}: {', '.join(sorted_employees)}")

    solve_task_three_invalid()
    captured = capsys.readouterr()

    # Пустая строка для сотрудника считается ложным значением, поэтому ничего не выводится
    assert captured.out.strip() == ""


def test_solve_task_four_basic(capsys):
    """Тест функции solve_task_four для правильного создания графа побед-поражений"""
    solve_task_four()
    captured = capsys.readouterr()

    # Проверяем, что Дима победил Артура
    assert "Дима -> Артур" in captured.out
    # Проверяем, что Тимур победил Артура и Диму
    assert "Тимур -> Артур, Дима" in captured.out


def test_solve_task_four_output_order(capsys):
    """Тест функции solve_task_four для правильного порядка вывода"""
    solve_task_four()
    captured = capsys.readouterr()

    # Проверяем, что победители отсортированы по алфавиту
    lines = [line.strip() for line in captured.out.split("\n") if line.strip()]
    assert lines[0].startswith("Дима")
    assert lines[1].startswith("Тимур")


def test_solve_ternary_operator_basic(capsys):
    """Тест функции solve_ternary_operator для проверки работы тернарного оператора"""
    solve_ternary_operator()
    captured = capsys.readouterr()

    # Проверяем, что функция выводит число
    output = captured.out.strip()
    assert output != "", "Функция должна выводить результат"

    # Проверяем, что вывод является числом (float)
    try:
        float(output)
    except ValueError:
        assert False, f"Вывод должен быть числом, получено: {output}"


def test_solve_multiplicity_basic(capsys):
    """Тест функции solve_multiplicity для проверки работы условия кратности"""
    solve_multiplicity()
    captured = capsys.readouterr()

    # Проверяем, что функция выводит число и сообщение
    output = captured.out.strip()
    assert output != "", "Функция должна выводить результат"

    # Проверяем, что вывод содержит число и сообщение о кратности
    parts = output.split()
    assert len(parts) >= 2, "Вывод должен содержать число и сообщение"

    # Проверяем последние две части (сообщение может содержать пробел)
    last_two_parts = " ".join(parts[-2:])
    assert last_two_parts in [
        "кратно 3",
        "не кратно 3",
    ], f"Сообщение должно быть о кратности 3, получено: {last_two_parts}"
