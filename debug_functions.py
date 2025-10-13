#!/usr/bin/env python3
from test_validator import TestValidator

validator = TestValidator()
results = validator.validate_tests()

print("Покрываемые функции:")
for test_name, result in results.items():
    print(f'{test_name}: {result["covered_functions"]}')
