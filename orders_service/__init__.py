import os
from pathlib import Path

from flask import Flask, jsonify
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from .models import Base, Order


def create_app(config=None):
    app = Flask(__name__)
    default_db = Path.cwd() / "instance" / "orders.sqlite3"
    db_path = Path(os.environ.get("ORDERS_DB", str(default_db))).resolve()
    app.config.update(DATABASE_URL=f"sqlite:///{db_path}",
                      SECRET_KEY=os.environ.get("ORDERS_SECRET", "local-recording-key-change-for-production"))
    app.config.update(config or {})
    if app.config["DATABASE_URL"].startswith("sqlite:///"):
        Path(app.config["DATABASE_URL"].removeprefix("sqlite:///")).parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(app.config["DATABASE_URL"])
    app.extensions["orders_engine"] = engine

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    # Prepared personal-extension slot; see preparation/PROVENANCE.txt.
    @app.get("/orders/<int:order_id>")
    def order_detail(order_id):
        with Session(engine) as session:
            order = session.get(Order, order_id)
            return (jsonify(order.to_dict()), 200) if order else (jsonify(error="Order not found"), 404)

    from .routes import register_orders
    register_orders(app, engine)
    return app
