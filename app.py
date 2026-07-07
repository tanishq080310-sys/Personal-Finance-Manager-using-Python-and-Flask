from models import db, User, Income, Expense, Goals, Savings
from flask import Flask, request, render_template, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import func
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from datetime import datetime
load_dotenv()

app = Flask(__name__)
password = quote_plus(os.getenv("Mysql_password"))
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:{password}@localhost/finance_manager"
app.config["SECRET_KEY"] = os.getenv("secret_key")

db.init_app(app)

login_manager = LoginManager(app)

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        existing_user = User.query.filter_by(Email = email).first()

        if existing_user:
            return "User already exists. Please Login"  
        else:
            new_user = User(Name = name, Email = email, Password = password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        
    return render_template("register.html")


@app.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(Email = email, Password = password).first()

        if existing_user:
            login_user(existing_user)
            return redirect(url_for("incomes"))
        else:
            return "Invalid Credentials. Please try again with correct email and password."
        
    return render_template("login.html")



@app.route("/incomes",methods = ["GET","POST"])
@login_required

def incomes():

    if request.method =="POST":
        amount = request.form.get("amount")
        source = request.form.get("source")
        payment_method = request.form.get("payment_method")
        description = request.form.get("description")
        date = request.form.get("date")
        category = request.form.get("category")

        new_income = Income(Amount = amount, Source = source, Payment_method = payment_method, description = description, Category = category, date = date, user_id = current_user.id)

        db.session.add(new_income)
        db.session.commit()
   
    incomes = Income.query.filter_by(user_id = current_user.id).all()

    total_income = 0

    for income in incomes:
        total_income = total_income + income.Amount


    return render_template("incomes.html", user = current_user, total_income = total_income, incomes = incomes)

@app.route("/delete_income/<int:income_id>", methods = ["POST"])
@login_required
def delete_income(income_id):
    income = Income.query.get(income_id)
    if income and income.user_id == current_user.id:
        db.session.delete(income)
        db.session.commit()

    return redirect(url_for("incomes"))



@app.route("/delete_all_incomes", methods = ["POST"])
@login_required
def delete_all_incomes():
    Income.query.filter_by(user_id = current_user.id).delete()
    db.session.commit()
    return redirect(url_for("incomes"))





@app.route("/dashboard")
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
    
    return render_template("dashboard.html",
        user = current_user, 
        total_income = total_income, 
        incomes = incomes, 
        total_expense = total_expense, 
        expenses = expenses, 
        Balance_amount = Balance_amount,
        recent_transactions = recent_transactions
    )


@app.route("/expenses",methods = ["GET","POST"])
@login_required
def expenses():
    
    if request.method == "POST":
        amount = request.form.get("amount")
        date = request.form.get("date")
        description = request.form.get("description")
        payment_method = request.form.get("payment_method")
        category = request.form.get("category")
    
        new_expense = Expense(date = date, amount = amount, payment_method = payment_method,description = description, category = category, user_id = current_user.id)

        db.session.add(new_expense)
        db.session.commit()

    total_expense = 0 

    expenses = Expense.query.filter_by(user_id = current_user.id).all()

    for expense in expenses:
        total_expense += expense.amount

    return render_template("expenses.html", user = current_user, total_expense = total_expense, expenses = expenses)

@app.route("/delete_expense/<int:expense_id>", methods = ["POST"])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if expense and expense.user_id == current_user.id:
        db.session.delete(expense)
        db.session.commit()
        return redirect(url_for("expenses"))
   

@app.route("/delete_all_expenses",methods = ["POST"])
@login_required
def delete_all_expenses():
    Expense.query.filter_by(user_id = current_user.id).delete()
    db.session.commit()
    return redirect(url_for("expenses"))



@app.route("/history")
@app.route("/filter_history",methods = ["GET","POST"])
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
        filtered_transactions = filtered_transactions
    )


@app.route("/goals",methods = ["GET","POST"])
@login_required
def goals():
    if request.method == "POST":
        name = request.form.get("name")
        target_amount = request.form.get("target_amount")
        description = request.form.get("description")
        deadline = request.form.get("deadline")
        goal_id = request.form.get("goal_id")
        goal_amount = request.form.get("goal_amount")
        deposited_date = request.form.get("deposited_date")
        note = request.form.get("note")

        if name:
            existing_goal = Goals.query.filter_by(user_id = current_user.id, name = name).first()
            if not existing_goal:
                new_goal = Goals(name = name, target_amount = target_amount, description = description, deadline = deadline, user_id = current_user.id)
                db.session.add(new_goal)
                db.session.commit()
        
        if goal_id and goal_amount and deposited_date:
            saved = Savings(amount = goal_amount, date = deposited_date, note = note, goal_id = goal_id, user_id = current_user.id)
            db.session.add(saved)
            db.session.commit()

    goal_totals = {}
    for goal in current_user.goals:
        goal_totals[goal.id] = sum(
            saving.amount for saving in goal.goal_savings
        )

    return render_template("goals.html",
        user = current_user,
        goal_totals = goal_totals
    )


                
            









@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))




with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug = True)