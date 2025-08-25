from flask import Flask
from models import db, User
from controllers.auth_controller import auth_bp
from controllers.product_controller import product_bp
from controllers.cart_controller import cart_bp
from controllers.admin_controller import admin_bp
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        
        admin_user = User.query.filter_by(email="admin@site.com").first()
        if not admin_user:
            hashed_password = generate_password_hash("1234")
            admin = User(
                name="Administrador", 
                email="admin@site.com", 
                password=hashed_password, 
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
