from datetime import datetime, timedelta
import pytest
from sqlalchemy import insert
from orders_service import create_app
from orders_service.models import Base, Order, STATUSES


@pytest.fixture
def app(tmp_path):
    app = create_app({"TESTING": True, "DATABASE_URL": f"sqlite:///{tmp_path / 'test.sqlite3'}",
                      "SECRET_KEY": "test-secret"})
    engine = app.extensions["orders_engine"]
    Base.metadata.create_all(engine)
    # This hook lets the same contract file be copied into the unmodified starter.
    try:
        from orders_service.pagination import apply_indexes
    except ImportError:
        pass
    else:
        apply_indexes(engine)
    with engine.begin() as conn:
        conn.execute(insert(Order), [
            {"customer": f"customer-{i}", "status": STATUSES[(i - 1) % 4],
             "total": (i % 5) * 100, "created_at": datetime(2026, 1, 1) + timedelta(hours=(i - 1) // 10)}
            for i in range(1, 81)
        ])
    yield app
    engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()
