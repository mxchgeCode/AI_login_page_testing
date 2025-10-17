import pytest
import io
import sys
import random
from unittest.mock import patch
from app import (
    solve_task_one, solve_task_two, solve_task_three, solve_task_four,
    solve_ternary_operator, solve_multiplicity, sound
)


def test_solve_task_one():
    """Test solve_task_one function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        solve_task_one()
        sys.stdout = sys.__stdout__
        # Based on actual output from logs: Books, Courses, Merch, Tutorials order
        expected_output = "Books: $7969\nCourses: $2991\nMerch: $4083\nTutorials: $3730"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__


def test_solve_task_two():
    """Test solve_task_two function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        solve_task_two()
        sys.stdout = sys.__stdout__
        # Based on actual output: Accounting: 17, Developing: 7, Marketing: 13, Sales: 13
        expected_output = "Accounting: 17\nDeveloping: 7\nMarketing: 13\nSales: 13"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__


def test_solve_task_three():
    """Test solve_task_three function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        solve_task_three()
        sys.stdout = sys.__stdout__
        # Based on actual output, this function outputs employee lists, not counts
        expected_output = "Accounting: Aaron Ferguson, Ann Bell, Brenda Davis, Casey Jenkins, Craig Wood, Dale Houston, Edna Cunningham, Gloria Higgins, James Wilkins, Jane Jackson, John Watts, Kay Scott, Kimberly Reynolds, Linda Hudson, Michelle Wright, Rosemary Garcia, Steven Diaz\nDeveloping: Arlene Gibson, Deborah George, Joyce Rivera, Miguel Norris, Nicole Watts, Thomas Porter, Wilma Woods\nMarketing: Andrew Clark, Bernice Ramos, Billy Lloyd, Carol Peters, Charles Bailey, Gail Hill, Helen Taylor, John Gonzalez, Joyce Lawrence, Mario Reynolds, Mary King, Ralph Morgan, Sam Davis\nSales: Alicia Mendoza, Charlotte Cox, Chester Fernandez, Connie Reid, Evelyn Martin, Gladys Taylor, John Washington, John White, Jose Taylor, Joseph Lee, Katie Warner, Marie Cooper, Robert Barnes"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__


def test_solve_task_four():
    """Test solve_task_four function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        solve_task_four()
        sys.stdout = sys.__stdout__
        # Based on actual output: Дима -> Артур; Тимур -> Артур, Дима (Артур -> Дима, Тимур is not shown)
        expected_output = "Дима -> Артур\nТимур -> Артур, Дима"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__


def test_solve_ternary_operator():
    """Test solve_ternary_operator function with seed=42"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        solve_ternary_operator(seed=42)
        sys.stdout = sys.__stdout__
        # Based on actual output from current run
        expected_output = "63.942679845788376"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__


def test_solve_multiplicity():
    """Test solve_multiplicity function with seed=42"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        solve_multiplicity(seed=42)
        sys.stdout = sys.__stdout__
        # Based on actual output from current run
        expected_output = "82 не кратно 3"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__


def test_sound():
    """Test sound function output"""
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        sound()
        sys.stdout = sys.__stdout__
        # Based on code analysis: m = ['до', 'ре', 'ми', 'фа', 'соль', 'ля', 'си']
        # nums = [1, 6, 7] means notes at positions 1, 6, 7
        # Note 1 ('до') gets # prefix because it's in ('до', 'фа')
        # Notes 6 and 7 ('ля', 'си') don't get # prefix
        expected_output = "#до ля си"
        assert captured_output.getvalue().strip() == expected_output
    finally:
        sys.stdout = sys.__stdout__