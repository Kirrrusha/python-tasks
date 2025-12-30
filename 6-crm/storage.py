from typing import List, Dict, Any

# Единое хранилище — глобальная переменная модуля
DATA: List[Dict[str, Any]] = []

def load() -> List[Dict[str, Any]]:
    """Возвращает копию данных (чтобы внешний код не мог их портить напрямую)."""
    return [
        {**item, "tags": set(item["tags"])}  # защищаем tags от мутации
        for item in DATA
    ]

def save(orders: List[Dict[str, Any]]) -> None:
    """Перезаписывает хранилище. Принимает список заказов."""
    global DATA
    # Конвертируем tags в list для единообразия при сохранении (но можно и set хранить — решаем ниже)
    # Давайте будем хранить tags как set внутри DATA (внутренне представление)
    DATA[:] = [
        {**order, "tags": set(order["tags"])}  # гарантируем set
        for order in orders
    ]