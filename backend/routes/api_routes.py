"""JSON and lightweight SSE for live order updates."""
import json
import time

from flask import Blueprint, Response, current_app, jsonify, stream_with_context
from flask_login import login_required

from models.entities import Order

bp = Blueprint("api", __name__)


@bp.route("/orders/summary")
@login_required
def orders_summary():
    active = Order.query.filter(~Order.status.in_(["Served", "Delivered"])).count()
    pending = Order.query.filter_by(status="Pending").count()
    return jsonify(
        {
            "active_orders": active,
            "pending": pending,
            "ts": time.time(),
        }
    )


@bp.route("/stream/orders")
@login_required
def stream_orders():
    """Server-Sent Events stream for kitchen/dashboard polling alternative."""
    interval = float(current_app.config.get("LIVE_REFRESH_SECONDS", 3))

    @stream_with_context
    def generate():
        while True:
            active = Order.query.filter(~Order.status.in_(["Served", "Delivered"])).count()
            payload = json.dumps({"active_orders": active, "ts": time.time()})
            yield f"data: {payload}\n\n"
            time.sleep(interval)

    return Response(generate(), mimetype="text/event-stream")
