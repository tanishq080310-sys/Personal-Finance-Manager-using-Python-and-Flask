from flask import Flask
from flask_login import LoginManager
from models import db, User
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

login_manager = LoginManager()

def create_app():

    load_dotenv()

    app = Flask(__name__)

    password = quote_plus(os.getenv("Mysql_password"))

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:{password}@localhost/finance_manager"

    app.config["SECRET_KEY"] = os.getenv("secret_key")

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from app.routes.auth import auth_bp
    from app.routes.income import income_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.expense import expense_bp
    from app.routes.goals import goals_bp
    from app.routes.history import history_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(income_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(history_bp)


    with app.app_context():
        db.create_all()

    return app

