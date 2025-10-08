import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class CodeTracker:
    """Класс для отслеживания изменений в коде приложения"""

    def __init__(self, config_file: str = "test_config.json"):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Загружает конфигурацию из файла"""
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_config(self):
        """Сохраняет конфигурацию в файл"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def calculate_file_hash(self, file_path: str) -> str:
        """Вычисляет SHA-256 хэш файла"""
        if not os.path.exists(file_path):
            return ""

        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def has_file_changed(self, file_path: str) -> bool:
        """Проверяет, изменился ли файл с момента последнего анализа"""
        current_hash = self.calculate_file_hash(file_path)
        hash_file = self.config.get("hash_file", "app_hash.txt")

        if not os.path.exists(hash_file):
            # Файл хэша не существует, создаем его
            self._save_hash(file_path, current_hash)
            return True

        with open(hash_file, "r") as f:
            previous_hash = f.read().strip()

        return current_hash != previous_hash

    def _save_hash(self, file_path: str, current_hash: str):
        """Сохраняет текущий хэш файла"""
        hash_file = self.config.get("hash_file", "app_hash.txt")
        with open(hash_file, "w") as f:
            f.write(current_hash)

        # Обновляем время последнего анализа
        self.config["last_analysis"] = datetime.now().isoformat()
        self._save_config()

    def update_hash(self, file_path: str):
        """Обновляет хэш файла после анализа"""
        current_hash = self.calculate_file_hash(file_path)
        self._save_hash(file_path, current_hash)

    def get_analysis_info(self) -> Dict:
        """Возвращает информацию о последнем анализе"""
        return {
            "last_analysis": self.config.get("last_analysis"),
            "current_hash": self.calculate_file_hash(
                self.config.get("app_file", "app.py")
            ),
            "previous_hash": self._get_previous_hash(),
        }

    def _get_previous_hash(self) -> str:
        """Получает предыдущий хэш из файла"""
        hash_file = self.config.get("hash_file", "app_hash.txt")
        if os.path.exists(hash_file):
            with open(hash_file, "r") as f:
                return f.read().strip()
        return ""

    def add_test_to_history(self, test_name: str, status: str, coverage: List[str]):
        """Добавляет информацию о тесте в историю"""
        if "test_history" not in self.config:
            self.config["test_history"] = []

        test_info = {
            "name": test_name,
            "status": status,
            "coverage": coverage,
            "timestamp": datetime.now().isoformat(),
        }

        self.config["test_history"].append(test_info)
        self._save_config()

    def get_test_history(self) -> List[Dict]:
        """Возвращает историю тестов"""
        return self.config.get("test_history", [])


def main():
    """Основная функция для тестирования"""
    tracker = CodeTracker()

    print("Информация об анализе:")
    info = tracker.get_analysis_info()
    for key, value in info.items():
        print(f"  {key}: {value}")

    print(f"\nФайл изменился: {tracker.has_file_changed('app.py')}")

    if tracker.has_file_changed("app.py"):
        print("Обновляем хэш...")
        tracker.update_hash("app.py")
        print("Хэш обновлен")


if __name__ == "__main__":
    main()
