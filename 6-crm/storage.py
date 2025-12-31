# storage.py
import json
import os
from typing import List

# Путь к файлу хранения (можно вынести в конфиг или параметр)
DATA_FILE = "orders.json"


def load() -> List[dict]:
    """
    Загружает заказы из JSON-файла.
    
    - Если файла нет — возвращает пустой список.
    - Если файл повреждён (невалидный JSON) — выводит понятное сообщение и возвращает [].
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Убеждаемся, что данные — список словарей (или хотя бы список)
            if isinstance(data, list):
                return data
            else:
                print(f"⚠️  Warning: {DATA_FILE} содержит некорректный формат: ожидался список, получен {type(data).__name__}. Возвращаем пустой список.")
                return []
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка чтения {DATA_FILE}: повреждённый JSON (строка {e.lineno}, колонка {e.colno}).", file=sys.stderr)
        print(f"   Подробности: {e.msg}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"❌ Непредвиденная ошибка при загрузке {DATA_FILE}: {type(e).__name__}: {e}", file=sys.stderr)
        return []


def save(items: List[dict]) -> None:
    """
    Сохраняет список заказов в JSON-файл.
    Перезаписывает файл. Создаёт его, если не существует.
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Ошибка при сохранении в {DATA_FILE}: {type(e).__name__}: {e}", file=sys.stderr)
        raise  # Можно не raise, если хотите «тихо проигнорировать» — но лучше знать о проблеме