from flask import request, redirect, render_template, Flask, Blueprint, url_for
from flask_login import login_required, current_user
from models import db, Income

income_bp = Blueprint("income", __name__)





@income_bp.route("/incomes",methods = ["GET","POST"])
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

@income_bp.route("/delete_income/<int:income_id>", methods = ["POST"])
@login_required
def delete_income(income_id):
    income = Income.query.get(income_id)
    if income and income.user_id == current_user.id:
        db.session.delete(income)
        db.session.commit()

    return redirect(url_for("income.incomes"))



@income_bp.route("/delete_all_incomes", methods = ["POST"])
@login_required
def delete_all_incomes():
    Income.query.filter_by(user_id = current_user.id).delete()
    db.session.commit()
    return redirect(url_for("income.incomes"))
