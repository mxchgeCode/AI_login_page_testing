import pytest
import io
import sys
from app import (
    solve_multiplicity,
    solve_task_three,
    sound,
    solve_task_one,
    solve_task_two,
    solve_task_four,
    solve_ternary_operator,
)


def test_solve_multiplicity():
    """Test {func_name} function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        solve_multiplicity()
        sys.stdout = sys.__stdout__
        # TODO: Replace with actual expected output
        expected_output = "EXPECTED_OUTPUT_HERE"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__


def test_solve_task_three():
    """Test {func_name} function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        solve_task_three()
        sys.stdout = sys.__stdout__
        # TODO: Replace with actual expected output
        expected_output = "EXPECTED_OUTPUT_HERE"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__


def test_sound():
    """Test {func_name} function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        sound()
        sys.stdout = sys.__stdout__
        # TODO: Replace with actual expected output
        expected_output = "EXPECTED_OUTPUT_HERE"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__


def test_solve_task_one():
    """Test {func_name} function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        solve_task_one()
        sys.stdout = sys.__stdout__
        # TODO: Replace with actual expected output
        expected_output = "EXPECTED_OUTPUT_HERE"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__


def test_solve_task_two():
    """Test {func_name} function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        solve_task_two()
        sys.stdout = sys.__stdout__
        # TODO: Replace with actual expected output
        expected_output = "EXPECTED_OUTPUT_HERE"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__


def test_solve_task_four():
    """Test {func_name} function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        solve_task_four()
        sys.stdout = sys.__stdout__
        # TODO: Replace with actual expected output
        expected_output = "EXPECTED_OUTPUT_HERE"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__


def test_solve_ternary_operator():
    """Test {func_name} function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        solve_ternary_operator()
        sys.stdout = sys.__stdout__
        # TODO: Replace with actual expected output
        expected_output = "EXPECTED_OUTPUT_HERE"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__

import pytest
import io
import sys
from unittest.mock import patch
from app import solve_task_one, solve_task_two, solve_task_three, solve_task_four, solve_ternary_operator, solve_multiplicity, sound

def test_solve_task_one():
    """Тест функции solve_task_one"""
    captured_output = io.StringIO()
    sys.stdout = captured_output
    solve_task_one()
    sys.stdout = sys.__stdout__
    expected_output = "Books: $1343\nMerch: $1145\nCourses: $966\nTutorials: $832\n"
    assert captured_output.getvalue() == expected_output

def test_solve_task_two():
    """Тест функции solve_task_two"""
    captured_output = io.StringIO()
    sys.stdout = captured_output
    solve_task_two()
    sys.stdout = sys.__stdout__
    expected_output = "Accounting: 12\nDeveloping: 5\nMarketing: 10\nSales: 11\n"
    assert captured_output.getvalue() == expected_output

def test_solve_task_three():
    """Тест функции solve_task_three"""
    captured_output = io.StringIO()
    sys.stdout = captured_output
    solve_task_three()
    sys.stdout = sys.__stdout__
    expected_output = "Accounting: Ann Bell, Aaron Ferguson, Ann Bell, Gloria Higgins, Casey Jenkins, Jane Jackson, Aaron Ferguson, Jane Jackson, Gloria Higgins, Craig Wood, Steven Diaz, Rosemary Garcia, John Watts, Brenda Davis, Steven Diaz, Michelle Wright, Dale Houston\nDeveloping: Miguel Norris, Wilma Woods, Wilma Woods, Nicole Watts, Thomas Porter, Deborah George, Deborah George, Arlene Gibson, Joyce Rivera, Thomas Porter, Wilma Woods, Deborah George, Arlene Gibson\nMarketing: Carol Peters, Ralph Morgan, Bernice Ramos, Joyce Lawrence, Mario Reynolds, Carol Peters, Ralph Morgan, Mary King, Andrew Clark, John Gonzalez, Carol Peters, Ralph Morgan, Mario Reynolds, Charles Bailey, Gail Hill, Casey Jenkins, Billy Lloyd, Sam Davis, Mary King, John Gonzalez, Charles Bailey, Mario Reynolds\nSales: Connie Reid, Jose Taylor, Jose Taylor, Charlotte Cox, Alicia Mendoza, Robert Barnes, Connie Reid, Joseph Lee, Evelyn Martin, Gladys Taylor, Charlotte Cox, John White, Marie Cooper, John White, Chester Fernandez, Alicia Mendoza, Katie Warner, Robert Barnes, Chester Fernandez, John Washington\n"
    assert captured_output.getvalue() == expected_output

def test_solve_task_four():
    """Тест функции solve_task_four"""
    captured_output = io.StringIO()
    sys.stdout = captured_output
    solve_task_four()
    sys.stdout = sys.__stdout__
    expected_output = "Тимур -> Дима, Артур\nДима -> Тимур, Артур\nАртур -> Тимур, Дима\n"
    assert captured_output.getvalue() == expected_output

def test_solve_ternary_operator():
    """Тест функции solve_ternary_operator"""
    with patch('random.seed') as mock_seed:
        mock_seed.return_value = None
        with patch('random.uniform') as mock_uniform:
            mock_uniform.return_value = 50
            captured_output = io.StringIO()
            sys.stdout = captured_output
            solve_ternary_operator()
            sys.stdout = sys.__stdout__
            assert captured_output.getvalue() == "50\n"

def test_solve_multiplicity():
    """Тест функции solve_multiplicity"""
    with patch('random.seed') as mock_seed:
        mock_seed.return_value = None
        with patch('random.randint') as mock_randint:
            mock_randint.return_value = 3
            captured_output = io.StringIO()
            sys.stdout = captured_output
            solve_multiplicity()
            sys.stdout = sys.__stdout__
            expected_output = "3 кратно 3\n"
            assert captured_output.getvalue() == expected_output

def test_sound():
    """Тест функции sound"""
    captured_output = io.StringIO()
    sys.stdout = captured_output
    sound()
    sys.stdout = sys.__stdout__
    expected_output = "до #ми ля #си\n"
    assert captured_output.getvalue() == expected_output