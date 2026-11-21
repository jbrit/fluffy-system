from flask import jsonify, request
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Order, STATUSES


def register_orders(app, engine):
    @app.get("/orders")
    def orders():
        status = request.args.get("status")
        if status is not None and status not in STATUSES:
            return jsonify(error="Invalid status"), 400
        query = select(Order).order_by(Order.created_at.desc(), Order.id.desc())
        if status is not None:
            query = query.where(Order.status == status)
        with Session(engine) as session:
            return jsonify([order.to_dict() for order in session.scalars(query)])
