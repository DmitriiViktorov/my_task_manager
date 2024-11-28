import json
from typing import Any
from pathlib import Path


class DataManager:
    def __init__(self, file_path: Path = Path("books.json") ):
        self.file_path = file_path

    def load_books(self) -> list[dict[str, Any]]:
        """Выгружает все данные из файла базы данных."""
        try:
            content = self.file_path.read_text()
            if not content.strip():
                return []
            return json.loads(content)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save_books(self, books: list[dict[str, Any]]) -> None:
        """Сохраняет полученные данные в файл базы данных."""
        self.file_path.write_text(json.dumps(books, indent=4, ensure_ascii=False))