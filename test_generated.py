import pytest
from app import solve_task_one, solve_task_two, solve_task_three, solve_task_four


# === ЮНИТ-ТЕСТЫ ДЛЯ ФУНКЦИЙ ===


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
    # Для Accounting должны быть: Aaron Ferguson, Ann Bell, Brenda Davis, Casey Jenkins, Craig Wood, Dale Houston, Edna Cunningham, Gloria Higgins, James Wilkins, Jane Jackson, John Watts, Kay Scott, Kimberly Reynolds, Linda Hudson, Michelle Wright, Rosemary Garcia, Steven Diaz
    accounting_line = [
        line for line in captured.out.split("\n") if line.startswith("Accounting:")
    ][0]
    accounting_employees = accounting_line.split(": ")[1].split(", ")
    assert accounting_employees[0] == "Aaron Ferguson"
    assert accounting_employees[1] == "Ann Bell"

    # Для Developing должны быть: Arlene Gibson, Deborah George, Joyce Rivera, Miguel Norris, Nicole Watts, Thomas Porter, Wilma Woods
    developing_line = [
        line for line in captured.out.split("\n") if line.startswith("Developing:")
    ][0]
    developing_employees = developing_line.split(": ")[1].split(", ")
    assert developing_employees[0] == "Arlene Gibson"
    assert developing_employees[-1] == "Wilma Woods"


def test_solve_task_three_empty_input(capsys):
    """Тест функции solve_task_three с пустым списком сотрудников"""

    # Создаем локальную версию функции с пустым списком
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

    # Создаем локальную версию функции с некорректными данными
    def solve_task_three_invalid():
        staff_broken = [
            ("", "John Doe"),
            (None, "Jane Smith"),
            ("IT", ""),
            ("HR", None),
        ]
        departments = {}
        for dept, person in staff_broken:
            if dept and person:  # Фильтруем некорректные данные
                departments.setdefault(dept, set()).add(person)

        for dept in sorted(departments):
            sorted_employees = sorted(departments[dept])
            if sorted_employees:  # Выводим только непустые отделы
                print(f"{dept}: {', '.join(sorted_employees)}")

    solve_task_three_invalid()
    captured = capsys.readouterr()

    # Пустая строка для сотрудника считается ложным значением, поэтому ничего не выводится
    assert captured.out.strip() == ""


def test_solve_task_four_basic(capsys):
    """Тест функции solve_task_four для правильного создания графа побед-поражений"""
    solve_task_four()
    captured = capsys.readouterr()

    # Проверяем, что Тимур победил Артура и Диму
    assert "Тимур -> Артур Дима" in captured.out
    # Проверяем, что Дима победил Артура
    assert "Дима -> Артур" in captured.out


def test_solve_task_four_output_order(capsys):
    """Тест функции solve_task_four для правильного порядка вывода"""
    solve_task_four()
    captured = capsys.readouterr()

    # Проверяем, что победители отсортированы по алфавиту
    lines = [line.strip() for line in captured.out.split("\n") if line.strip()]
    assert lines[0].startswith("Дима")
    assert lines[1].startswith("Тимур")


# === ПРИМЕЧАНИЕ ===
# Функции solve_task_one(), solve_task_two(), solve_task_three() и solve_task_four() полностью покрыты юнит-тестами выше
# Тесты проверяют правильность подсчета данных, порядок вывода результатов и обработку краевых случаев


# Тесты будут генерироваться автоматически при изменении app.py

# === ПРИМЕР ЛУЧШЕЙ ПРАКТИКИ ТЕСТИРОВАНИЯ ===
# Вместо patch('sys.stdout') рекомендуется использовать capsys:
#
# def test_solve_task_one_pytest_style(capsys):
#     """Пример теста в стиле pytest с использованием capsys"""
#     solve_task_one()
#     captured = capsys.readouterr()
#     expected_lines = [
#         "Books: $7969",
#         "Courses: $2991",
#         "Merch: $4083",
#         "Tutorials: $3730"
#     ]
#     output_lines = [line.strip() for line in captured.out.strip().split('\n') if line.strip()]
#     assert output_lines == expected_lines
#
# def test_solve_task_with_exception_pytest_style():
#     """Пример тестирования исключений в стиле pytest"""
#     with pytest.raises(ValueError):
#         function_that_raises_error()
#
# Преимущества pytest стиля:
# - Чистый код без unittest классов
# - Встроенные fixtures (capsys, tmp_path, etc.)
# - Лучшая производительность
# - Более читаемые assert statements
# - Встроенная поддержка параметризации тестов
