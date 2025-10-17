#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
from app import (
    solve_task_one, solve_task_two, solve_task_three, solve_task_four,
    solve_ternary_operator, solve_multiplicity, sound
)

def capture_output(func):
    """Capture function output"""
    old_stdout = sys.stdout
    sys.stdout = captured = io.StringIO()
    try:
        func()
        return captured.getvalue().strip()
    finally:
        sys.stdout = old_stdout

print("=== Testing function outputs ===")

print("\n1. solve_task_one():")
output1 = capture_output(solve_task_one)
print(repr(output1))

print("\n2. solve_task_two():")
output2 = capture_output(solve_task_two)
print(repr(output2))

print("\n3. solve_task_three():")
output3 = capture_output(solve_task_three)
print(repr(output3))

print("\n4. solve_task_four():")
output4 = capture_output(solve_task_four)
print(repr(output4))

print("\n5. solve_ternary_operator(seed=42):")
output5 = capture_output(lambda: solve_ternary_operator(seed=42))
print(repr(output5))

print("\n6. solve_multiplicity(seed=42):")
output6 = capture_output(lambda: solve_multiplicity(seed=42))
print(repr(output6))

print("\n7. sound():")
output7 = capture_output(sound)
print(repr(output7))