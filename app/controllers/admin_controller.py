from flask import Blueprint, render_template, redirect, url_for, session
from models import Order

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/orders")
def admin_orders():
    if session.get("role") != "admin":
        return redirect(url_for("product.marketplace"))
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin_orders.html", orders=orders)
