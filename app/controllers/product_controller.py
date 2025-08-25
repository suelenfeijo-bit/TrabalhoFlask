from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Product

product_bp = Blueprint("product", __name__)

@product_bp.route("/marketplace")
def marketplace():
    if "user_id" not in session:
        return redirect(url_for("auth.index"))
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("index.html", products=products, user_role=session.get("role"))

@product_bp.route("/add_product", methods=["GET", "POST"])
def add_product():
    if session.get("role") != "admin":
        return redirect(url_for("product.marketplace"))

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = int(float(request.form["price"]) * 100)
        db.session.add(Product(name=name, description=description, price_cents=price))
        db.session.commit()
        return redirect(url_for("product.marketplace"))

    return render_template("add_product.html")
