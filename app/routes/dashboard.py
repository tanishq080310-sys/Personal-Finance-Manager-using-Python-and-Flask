from flask import Blueprint,redirect, render_template,url_for
from flask_login import login_required, current_user
from models import Income, Expense, Savings



dashboard_bp = Blueprint("dashboard",__name__)



@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    
    
    incomes = Income.query.filter_by(user_id = current_user.id).all()
    total_income = 0
    for income in incomes:
        total_income = total_income + income.Amount

    expenses = Expense.query.filter_by(user_id = current_user.id).all()
    total_expense = 0
    for expense in expenses:
        total_expense += expense.amount

    Balance_amount = total_income - total_expense

    transactions = []
    for income in incomes:
        transactions.append({
            "Date": income.date,
            "Amount": income.Amount,
            "Type": "Income",
            "Category": income.Category
        })
    for expense in expenses:
        transactions.append({
            "Date": expense.date,
            "Amount": expense.amount,
            "Type": "Expense",
            "Category": expense.category
        })
    transactions.sort(key=lambda x: x["Date"], reverse=True)
    recent_transactions = transactions[:3]

    savings = Savings.query.filter_by(user_id = current_user.id).all()
    total_saving = 0
    for saving in savings:
        total_saving += saving.amount

    Balance_amount = total_income - total_expense - total_saving

    
    return render_template("dashboard.html",
        user = current_user, 
        total_income = total_income, 
        incomes = incomes, 
        total_expense = total_expense, 
        expenses = expenses, 
        Balance_amount = Balance_amount,
        recent_transactions = recent_transactions,
        savings = savings,
        total_saving = total_saving
    )
