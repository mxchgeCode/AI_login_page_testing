import pytest
from playwright.sync_api import sync_playwright
import unittest.mock as mock


# === ЮНИТ-ТЕСТЫ ДЛЯ ФУНКЦИЙ ===
def test_add_positive():
    """Тест функции add с положительными числами"""
    from app import add

    result = add(2, 3)
    assert result == 5


def test_add_negative():
    """Тест функции add с отрицательными числами"""
    from app import add

    result = add(-1, -2)
    assert result == -3


def test_add_zero():
    """Тест функции add с нулевыми значениями"""
    from app import add

    result = add(0, 0)
    assert result == 0


def test_add_mixed():
    """Тест функции add со смешанными значениями"""
    from app import add

    result = add(10, -5)
    assert result == 5


# === ИНТЕГРАЦИОННЫЕ ТЕСТЫ ДЛЯ БРАУЗЕРНЫХ ФУНКЦИЙ ===
def test_login_wrapper():
    """Wrapper для вызова test_login из app.py"""
    from app import test_login

    test_login()


def test_negative_username_wrapper():
    """Wrapper для вызова test_negative_username из app.py"""
    from app import test_negative_username

    test_negative_username()


def test_negative_password_wrapper():
    """Wrapper для вызова test_negative_password из app.py"""
    from app import test_negative_password

    test_negative_password()


# === ПРИМЕЧАНИЕ ===
# Мокинг-тесты для браузерных функций сложны из-за архитектуры Playwright
# Интеграционные тесты (wrapper) обеспечивают достаточное покрытие
# Для полного тестирования браузерных взаимодействий используются реальные тесты


# Тесты будут генерироваться автоматически при изменении app.py
# Для работы этого файла убедитесь, что установлен playwright:
# pip install playwright
# playwright install chromium
