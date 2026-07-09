from flask import redirect, render_template, url_for,request,Blueprint
from flask_login import login_required, current_user
from models import db, Expense

expense_bp = Blueprint("expense",__name__)


@expense_bp.route("/expenses",methods = ["GET","POST"])
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

@expense_bp.route("/delete_expense/<int:expense_id>", methods = ["POST"])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if expense and expense.user_id == current_user.id:
        db.session.delete(expense)
        db.session.commit()
        return redirect(url_for("expense.expenses"))
   

@expense_bp.route("/delete_all_expenses",methods = ["POST"])
@login_required
def delete_all_expenses():
    Expense.query.filter_by(user_id = current_user.id).delete()
    db.session.commit()
    return redirect(url_for("expense.expenses"))
