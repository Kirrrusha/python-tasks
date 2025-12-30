from datetime import datetime, timezone
from typing import List, Optional, Set, Dict, Any
from . import storage

def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def create_order(
    title: str,
    amount: float,
    email: str,
    status: str = "new",
    tags: Optional[Set[str]] = None,
    due: Optional[str] = None
) -> Dict[str, Any]:
    if tags is None:
        tags = set()
    valid_statuses = {"new", "in_progress", "done", "cancelled"}
    if status not in valid_statuses:
        raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")

    orders = storage.load()
    order_id = max((o["id"] for o in orders), default=0) + 1

    new_order = {
        "id": order_id,
        "title": title,
        "amount": float(amount),
        "email": email,
        "status": status,
        "tags": set(tags),
        "created_at": _now_utc_iso(),
        "due": due,
        "closed_at": None
    }

    orders.append(new_order)
    storage.save(orders)
    return new_order


def list_orders() -> List[Dict[str, Any]]:
    return storage.load()


def edit_order(
    order_id: int,
    title: Optional[str] = None,
    amount: Optional[float] = None,
    email: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[Set[str]] = None,
    due: Optional[str] = None
) -> Dict[str, Any]:
    orders = storage.load()
    for order in orders:
        if order["id"] == order_id:
            if title is not None:
                order["title"] = title
            if amount is not None:
                order["amount"] = float(amount)
            if email is not None:
                order["email"] = email
            if status is not None:
                valid_statuses = {"new", "in_progress", "done", "cancelled"}
                if status not in valid_statuses:
                    raise ValueError(f"Invalid status: {status}")
                order["status"] = status
                if status in {"done", "cancelled"} and order["closed_at"] is None:
                    order["closed_at"] = _now_utc_iso()
                elif status in {"new", "in_progress"} and order["closed_at"] is not None:
                    order["closed_at"] = None
            if tags is not None:
                order["tags"] = set(tags)
            if due is not None:
                order["due"] = due
            storage.save(orders)
            return {**order, "tags": set(order["tags"])}
    raise ValueError(f"Order with id {order_id} not found")


def remove_order(order_id: int) -> None:
    orders = storage.load()
    new_orders = [o for o in orders if o["id"] != order_id]
    if len(new_orders) == len(orders):
        raise ValueError(f"Order with id {order_id} not found")
    storage.save(new_orders)