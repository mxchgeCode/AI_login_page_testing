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
        # Calculate expected values based on the code analysis
        # Books: 1343 + 1166 + 848 + 815 + 1218 + 1003 + 920 + 656 = 7969
        # Merch: 616 + 1145 + 642 + 951 + 729 = 4083
        # Courses: 966 + 1061 + 964 = 2991
        # Tutorials: 832 + 1041 + 880 + 977 = 3730
        expected_output = "Books: $7969\nMerch: $4083\nCourses: $2991\nTutorials: $3730"
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
        # Count employees by department based on code analysis
        # Accounting: 15, Developing: 7, Marketing: 11, Sales: 13
        expected_output = "Accounting: 15\nDeveloping: 7\nMarketing: 11\nSales: 13"
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
        # Based on code analysis, this function finds unique employees in each department
        # Accounting: 17 unique employees
        # Developing: 7 unique employees
        # Marketing: 13 unique employees
        # Sales: 13 unique employees
        expected_output = "Accounting: 17\nDeveloping: 7\nMarketing: 13\nSales: 13"
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
        # Based on code analysis: pairs = [("Тимур", "Артур"), ("Тимур", "Дима"), ("Дима", "Артур")]
        # Creates a graph where arrows show who beats whom
        # Sorted by winner names: Артур -> Дима, Тимур; Дима -> Артур; Тимур -> Артур, Дима
        expected_output = "Артур -> Дима, Тимур\nДима -> Артур\nТимур -> Артур, Дима"
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
        # With seed=42, we get deterministic results
        expected_output = "42.75288153584405"
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
        # With seed=42, we get deterministic results
        expected_output = "42 не кратно 3"
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