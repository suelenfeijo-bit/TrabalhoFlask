from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name", "").strip()

        if action == "login":
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session["user_id"] = user.id
                session["role"] = user.role
                return redirect(url_for("product.marketplace"))
            # Senha incorreta ou usuário não encontrado
            return render_template("incorrect_password.html")  # ← Aqui

        elif action == "signup":
            if not name:
                return render_template("error.html", message="Digite seu nome!")  # opcional
            if not password:
                return render_template("error.html", message="Digite uma senha!")  # opcional
            if User.query.filter_by(email=email).first():
                return render_template("email_exists.html")  # ← Aqui

            hashed_password = generate_password_hash(password)
            user = User(name=name, email=email, password=hashed_password, role="client")
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            session["role"] = "client"
            return render_template("registration_success.html")  # ← Aqui

    return render_template("login.html")
