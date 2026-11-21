from datetime import datetime, timedelta

from sqlalchemy import func, insert, select
from .models import Base, Order, STATUSES


def seed(engine, rows=100_000):
    Base.metadata.create_all(engine)
    with engine.begin() as conn:
        if conn.scalar(select(func.count()).select_from(Order)):
            raise ValueError("Refusing to seed a non-empty database; use a new ORDERS_DB path")
        origin = datetime(2026, 1, 1)
        for start in range(0, rows, 5_000):
            conn.execute(insert(Order), [
                {"customer": f"customer-{i % 1200:04d}",
                 "status": STATUSES[(i - 1) % len(STATUSES)],
                 "total": (i * 37 % 500) * 100,
                 "created_at": origin + timedelta(minutes=(i - 1) // 50)}
                for i in range(start + 1, min(start + 5_000, rows) + 1)
            ])
    return rows
