import pytest
from playwright.sync_api import sync_playwright
from app import test_login, test_negative_username, test_negative_password


def test_login_wrapper():
    """Wrapper для вызова test_login из app.py"""
    test_login()


def test_negative_username_wrapper():
    """Wrapper для вызова test_negative_username из app.py"""
    test_negative_username()


def test_negative_password_wrapper():
    """Wrapper для вызова test_negative_password из app.py"""
    test_negative_password()


# Тесты будут генерироваться автоматически при изменении app.py
# Для работы этого файла убедитесь, что установлен playwright:
# pip install playwright
# playwright install chromium
