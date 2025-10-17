#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys

def run_tests():
    """Run tests and return results"""
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "test_generated.py", "-v", "--tb=short"
        ], capture_output=True, text=True, encoding='utf-8')

        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print(f"Return code: {result.returncode}")

        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    print(f"\nTests {'PASSED' if success else 'FAILED'}")