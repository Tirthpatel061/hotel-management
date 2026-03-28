"""
Hotel Management System — Flask application entry (MVC: Models / routes / templates).
Run from the `backend` folder:  python app.py
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

# Ensure `backend` is on path when running `python app.py` from this directory
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

load_dotenv(BACKEND_DIR / ".env")

from config import Config
from extensions import db, login_manager
from models.entities import User


def create_app(config_class=Config):
    project_root = BACKEND_DIR.parent
    app = Flask(
        __name__,
        template_folder=str(project_root / "frontend" / "templates"),
        static_folder=str(project_root / "frontend" / "static"),
        static_url_path="/static",
    )
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def _unauthorized():
        from flask import redirect, request, url_for

        return redirect(url_for("auth.login", next=request.path))

    # Blueprints
    from routes.auth_routes import bp as auth_bp
    from routes.dashboard_routes import bp as dash_bp
    from routes.order_routes import bp as order_bp
    from routes.kitchen_routes import bp as kitchen_bp
    from routes.menu_routes import bp as menu_bp
    from routes.billing_routes import bp as billing_bp
    from routes.staff_routes import bp as staff_bp
    from routes.attendance_routes import bp as att_bp
    from routes.salary_routes import bp as salary_bp
    from routes.reports_routes import bp as reports_bp
    from routes.api_routes import bp as api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(order_bp, url_prefix="/orders")
    app.register_blueprint(kitchen_bp, url_prefix="/kitchen")
    app.register_blueprint(menu_bp, url_prefix="/menu")
    app.register_blueprint(billing_bp, url_prefix="/billing")
    app.register_blueprint(staff_bp, url_prefix="/staff")
    app.register_blueprint(att_bp, url_prefix="/attendance")
    app.register_blueprint(salary_bp, url_prefix="/salary")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.context_processor
    def inject_brand():
        from brand_data import (
            ESTABLISHED_YEAR,
            MENU_PDF_URL,
            OUTLETS,
            TAGLINE_MENU_CARD,
            WEBSITE_URL,
            WHATSAPP_URL,
        )

        return {
            "brand_name": app.config.get("BRAND_NAME", "Swagat Corner"),
            "brand_tagline": app.config.get("BRAND_TAGLINE", ""),
            "brand_tagline_2": TAGLINE_MENU_CARD,
            "brand_logo": app.config.get("BRAND_LOGO", "images/swagat-logo.png"),
            "brand_website": WEBSITE_URL,
            "brand_menu_pdf": MENU_PDF_URL,
            "brand_whatsapp": WHATSAPP_URL,
            "brand_since": ESTABLISHED_YEAR,
            "brand_outlets": OUTLETS,
        }

    with app.app_context():
        # Create tables if missing (dev convenience; production should use migrations)
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
