def test_health(client):
    assert client.get("/health").json == {"status": "ok"}


def test_orders_are_bare_array(client):
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 80


def test_newest_first(client):
    rows = client.get("/orders").json
    assert [r["id"] for r in rows] == list(range(80, 0, -1))


def test_status_filter(client):
    rows = client.get("/orders?status=paid").json
    assert len(rows) == 20
    assert all(r["status"] == "paid" for r in rows)


def test_invalid_status(client):
    assert client.get("/orders?status=unknown").status_code == 400


def test_order_detail(client):
    row = client.get("/orders/1").json
    assert row == {"id": 1, "customer": "customer-1", "status": "pending", "total": 100,
                   "created_at": "2026-01-01T00:00:00.000000Z"}


def test_missing_order(client):
    assert client.get("/orders/9999").status_code == 404


def test_order_fields(client):
    assert set(client.get("/orders").json[0]) == {"id", "customer", "status", "total", "created_at"}
