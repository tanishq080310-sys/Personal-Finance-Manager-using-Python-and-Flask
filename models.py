from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(100), nullable = False)
    Email = db.Column(db.String(100), unique = True, nullable = False)
    Password = db.Column(db.String(100), nullable = False)
    incomes = db.relationship("Income", backref = "user", lazy = True)
    expenses = db.relationship("Expense", backref = "user", lazy = True)


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




    

