from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import UserMixin
from datetime import date, datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(100), nullable = False)
    Email = db.Column(db.String(100), unique = True, nullable = False)
    Password = db.Column(db.String(100), nullable = False)
    incomes = db.relationship("Income", backref = "user", lazy = True)
    expenses = db.relationship("Expense", backref = "user", lazy = True)
    goals = db.relationship("Goals",backref="user",lazy = True)
    savings = db.relationship("Savings", backref = "user", lazy = True)


class Income(db.Model, UserMixin):
    __tablename__ = "income"
    id = db.Column(db.Integer, primary_key = True)
    Amount = db.Column(db.Float, nullable = False)
    Source = db.Column(db.String(100), nullable = False)
    Payment_method = db.Column(db.String(100))
    description = db.Column(db.String(100))
    Category = db.Column(db.String(100))
    date = db.Column(db.Date, default = date.today, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable = False)

class Expense(db.Model, UserMixin):
    __tablename__ = "expense"
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float, nullable = False)
    description = db.Column(db.String(100))
    payment_method = db.Column(db.String(100))
    date = db.Column(db.Date, default = date.today, nullable = False)
    category = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

class Goals(db.Model, UserMixin):
    __tablename__ = "goal"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100),nullable = False)
    target_amount = db.Column(db.Float, nullable = False)
    current_amount = db.Column(db.Float)
    deadline = db.Column(db.Date)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default = datetime.today)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    goal_savings = db.relationship("Savings", backref = "goal",lazy = True)

class Savings(db.Model, UserMixin):
    __tablename__ = "savings"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float,nullable = False)
    note = db.Column(db.String(150))
    date = db.Column(db.Date, default = date.today)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))





    

