from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from models import db, Income, Expense, Savings, Goals
from sqlalchemy import func
from datetime import datetime



history_bp = Blueprint("history",__name__)

@history_bp.route("/history",methods = ["GET", "POST"])
@login_required
def history():

    incomes = Income.query.filter_by(user_id = current_user.id).all()
    expenses = Expense.query.filter_by(user_id = current_user.id).all()

    transactions = []

    for income in incomes:
        transactions.append({
            "Date" : income.date,
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

    transactions.sort(key = lambda x:x["Date"], reverse= True)

    max_income = db.session.query(func.max(Income.Amount)).filter_by(user_id = current_user.id).scalar()

    max_expense = db.session.query(func.max(Expense.amount)).filter_by(user_id = current_user.id).scalar()



    total_transactions = len(transactions)
    income_transactions = 0
    expense_transactions = 0

    for a in transactions:
        x = a.get("Type")
        if x == "Income":
            income_transactions += 1
        elif x == "Expense":
            expense_transactions += 1


    filtered_transactions = []

    history_savings = []

    savings = Savings.query.filter_by(user_id = current_user.id).all()
    
    for saving in savings:
        goal_name = saving.goal_id
        goals = Goals.query.get(goal_name)
        goalname = goals.name

        history_savings.append({
            "Date": saving.date,
            "Amount": saving.amount,
            "Note" : saving.note,
            "Goal_Name" : goalname
        })



    if request.method == "POST":
        print("Form reveived")
        date = request.form.get("date")
        amount = request.form.get("amount")
        type = request.form.get("type")

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()

        for transaction in transactions:
            if date and transaction["Date"] != date:
                continue
            if amount and transaction["Amount"] != float(amount):
                continue
            if type and transaction["Type"] != type:
                continue
            filtered_transactions.append(transaction)

        print(date)
        print(amount)
        print(type)
        print(filtered_transactions)    

   

    return render_template(
        "history.html", 
        transactions = transactions, 
        total_transactions = total_transactions, 
        income_transactions = income_transactions,
        expense_transactions = expense_transactions,
        max_income = max_income,
        max_expense = max_expense,
        filtered_transactions = filtered_transactions,
        user = current_user,
        history_savings = history_savings
    )
