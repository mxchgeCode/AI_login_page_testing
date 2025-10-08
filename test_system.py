#!/usr/bin/env python3
"""
Простой скрипт для демонстрации работы системы автоматического тестирования
"""

import os
import sys
from smart_test_generator import SmartTestGenerator
from test_runner import TestRunner


def demo():
    """Демонстрация работы системы"""
    print("🚀 Демонстрация системы автоматического тестирования")
    print("=" * 60)

    # Проверяем наличие API ключа
    if not os.getenv("OPENROUTER_API_KEY"):
        print("⚠️  Предупреждение: OPENROUTER_API_KEY не установлен")
        print("   Генерация тестов может не работать")
        print()

    # Создаем генератор тестов
    print("1️⃣ Создание генератора тестов...")
    generator = SmartTestGenerator()

    # Проверяем изменения
    print("2️⃣ Проверка изменений в коде...")
    app_file = generator.config.get('app_file', 'app.py')
    if generator.tracker.has_file_changed(app_file):
        print("   ✅ Обнаружены изменения в коде")
    else:
        print("   ℹ️  Изменений в коде не обнаружено")

    # Генерируем тесты
    print("3️⃣ Генерация/обновление тестов...")
    success = generator.run_full_cycle()

    if success:
        print("   ✅ Тесты успешно сгенерированы/обновлены")
    else:
        print("   ⚠️  Проблемы при генерации тестов")

    # Запускаем тесты
    print("4️⃣ Запуск тестов...")
    runner = TestRunner()
    results = runner.run_tests_only()

    print("   📊 Результаты:")
    print(f"   Тесты пройдены: {'✅' if results['tests_passed'] else '❌'}")
    print(f"   Стиль кода: {'✅' if results['linting_passed'] else '❌'}")

    print()
    print("🎯 Демонстрация завершена!")
    print("=" * 60)

    # Возвращаем код выхода для CI/CD
    return 0 if results['tests_passed'] else 1


if __name__ == "__main__":
    sys.exit(demo())