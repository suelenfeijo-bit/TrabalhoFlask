from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User, Product, Order, OrderItem, Payment

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if session.get("role") != "client":
        return redirect(url_for("product.marketplace"))

    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    # redireciona para a view_cart (novo nome)
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/cart")
def view_cart():
    if session.get("role") != "client":
        return redirect(url_for("product.marketplace"))

    cart = session.get("cart", {})
    products = []
    total_cents = 0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            products.append({"product": product, "quantity": qty})
            total_cents += product.price_cents * qty
    return render_template("cart.html", products=products, total_cents=total_cents)

@cart_bp.route("/checkout", methods=["POST"])
def checkout():
    if session.get("role") != "client":
        return redirect(url_for("product.marketplace"))

    cart = session.get("cart", {})
    if not cart:
        return redirect(url_for("product.marketplace"))

    user = User.query.get(session["user_id"])
    total_cents = 0
    order = Order(user_id=user.id, total_cents=0)
    db.session.add(order)
    db.session.commit()

    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=qty,
                unit_price_cents=product.price_cents
            )
            db.session.add(item)
            total_cents += product.price_cents * qty

    order.total_cents = total_cents
    payment = Payment(order_id=order.id)
    db.session.add(payment)
    db.session.commit()

    session.clear()
    return render_template("success.html", order=order)
