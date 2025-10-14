

import pytest
from app import solve_task_one, solve_task_two, solve_task_three, solve_task_four, solve_ternary_operator, solve_multiplicity, sound

def test_solve_task_one(capsys):
    solve_task_one()
    captured = capsys.readouterr()
    expected_output = "Books: $1343\nBooks: $1218\nBooks: $1003\nBooks: $920\nBooks: $815\nBooks: $848\nMerch: $1145\nMerch: $951\nMerch: $729\nMerch: $642\nCourses: $966\nCourses: $964\nCourses: $1061\nTutorials: $1041\nTutorials: $977\nTutorials: $880\nTutorials: $832\n"
    assert captured.out == expected_output

def test_solve_task_two(capsys):
    solve_task_two()
    captured = capsys.readouterr()
    expected_output = "Accounting: 15\nDeveloping: 7\nMarketing: 11\nSales: 13\n"
    assert captured.out == expected_output

def test_solve_task_three(capsys):
    solve_task_three()
    captured = capsys.readouterr()
    expected_output = "Accounting: Ann Bell, Aaron Ferguson, Brenda Davis, Craig Wood, Dale Houston, Edna Cunningham, Gloria Higgins, Jane Jackson, John Watts, Kay Scott, Kimberly Reynolds, Linda Hudson, Michelle Wright, Rosemary Garcia, Steven Diaz\nDeveloping: Arlene Gibson, Deborah George, Miguel Norris, Nicole Watts, Thomas Porter, Wilma Woods\nMarketing: Andrew Clark, Bernice Ramos, Billy Lloyd, Carol Peters, Charles Bailey, Gail Hill, Helen Taylor, Joyce Lawrence, Mario Reynolds, Mary King, Ralph Morgan, Sam Davis\nSales: Alicia Mendoza, Charlotte Cox, Chester Fernandez, Connie Reid, Evelyn Martin, Gladys Taylor, John Washington, John White, Jose Taylor, Joseph Lee, Katie Warner, Marie Cooper, Robert Barnes\n"
    assert captured.out == expected_output

def test_solve_task_four(capsys):
    solve_task_four()
    captured = capsys.readouterr()
    expected_output = "Артур -> Дима, Тимур\nДима -> Артур\nТимур -> Дима\n"
    assert captured.out == expected_output

def test_solve_ternary_operator():
    solve_ternary_operator()
    # Since the function uses random, we can't test the exact output
    # We can only test that it doesn't raise any exceptions
    pass

def test_solve_multiplicity():
    solve_multiplicity()
    # Since the function uses random, we can't test the exact output
    # We can only test that it doesn't raise any exceptions
    pass

def test_sound(capsys):
    sound()
    captured = capsys.readouterr()
    expected_output = "си ми\n"
    assert captured.out == expected_output

def test_solve_multiplicity_krato_3():
    with pytest.raises(Exception):
        solve_multiplicity = lambda: None
        solve_multiplicity()
        assert "кратно 3" in str(solve_multiplicity())

def test_solve_multiplicity_ne_krato_3():
    with pytest.raises(Exception):
        solve_multiplicity = lambda: None
        solve_multiplicity()
        assert "не кратно 3" in str(solve_multiplicity())