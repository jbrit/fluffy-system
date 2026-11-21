# Orders service: working starting repository

A prepared Flask + SQLAlchemy + SQLite service for an inherited-code exercise.
The pagination design is intentionally undecided. The existing behavior is correct:
`GET /orders` returns every order as a bare array, newest first with ID as a tie
breaker. `?status=paid` filters it; `GET /orders/1` is the prepared extension.
Totals are integer cents, timestamps are UTC, and there are no pagination indexes.

Use Python 3.11+ (the measured environment uses 3.14.6). From this directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m orders_service serve
```

The supplied `instance/orders.sqlite3` has 100,000 deterministic orders, 2,000
shared timestamps and 500 shared totals. If the database is absent, run
`.venv/bin/python -m orders_service seed --rows 100000` before serving. Seeding
refuses to overwrite existing rows. For a second database, set `ORDERS_DB` to a
new absolute path. The local server binds to `127.0.0.1:5000`.

```sh
curl -sS http://127.0.0.1:5000/health
curl -sS 'http://127.0.0.1:5000/orders?status=paid'
```
