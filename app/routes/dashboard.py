from flask import Blueprint,redirect, render_template,url_for, request
from flask_login import login_required, current_user
from models import Income, Expense, Savings, Goals
from ai import ai_summary


dashboard_bp = Blueprint("dashboard",__name__)



@dashboard_bp.route("/dashboard", methods = ["GET", "POST"])
@login_required
def dashboard():
    
    
    incomes = Income.query.filter_by(user_id = current_user.id).all()
    total_income = 0
    for income in incomes:
        total_income = total_income + income.Amount

    expenses = Expense.query.filter_by(user_id = current_user.id).all()
    expense_category = {}
    total_expense = 0

    for expense in expenses:
        category = expense.category
        total_expense += expense.amount
        if category not in expense_category:
            expense_category[category] = 0
        expense_category[category] = expense.amount


       

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
    
    goals = Goals.query.filter_by(user_id = current_user.id).all()

    goals_data = []
    for goal in goals:
        goals_data.append({
            "Goal_Name": goal.name,
            "Target_amount": goal.target_amount,
            "Current_amount": goal.current_amount
        })

    Balance_amount = total_income - total_expense - total_saving

    btn_clicked = "False"
    error = None
    status = None
    score = None
    summary_health = None
    highest_category = None
    highest_category_amount = None
    category_breakdown = None
    Goal_name = None
    Target_amount = None
    Current_amount = None
    completion_percentage = None
    Goal_status = None
    observation = None
    recommendation = None
    summary_ai = None

    if request.method == "POST":

        ai_data = {
            "Income": {
                "total": total_income
            },
            "Expense": {
                "total": total_expense,
                "categories": expense_category
            },
            "Savings": {
                "total": total_saving
            },
            "Goals": goals_data
        }
    
        if "generate_ai" in request.form:
            generated_content = ai_summary(ai_data)

            if generated_content.get("error"):
                btn_clicked = "True"
                error = generated_content.get("error")
            else:
                btn_clicked = "True"
                fh = generated_content.get("financial_health", {})
                status = fh.get("status")
                score = fh.get("score")
                summary_health = fh.get("summary")
                ea = generated_content.get("expense_analysis", {})
                highest_category = ea.get("highest_category")
                highest_category_amount = ea.get("highest_category_amount")
                category_breakdown = ea.get("category_breakdown")
                gp = generated_content.get("goal_progress", [])
                for g in gp:
                    Goal_name = g.get("goal_name")
                    Target_amount = g.get("target_amount")
                    Current_amount = g.get("current_amount")
                    completion_percentage = g.get("completion_percentage")
                    Goal_status = g.get("status")
                observation = ", ".join(generated_content.get("observations", []))
                recommendation = ", ".join(generated_content.get("recommendations", []))
                summary_ai = ", ".join(generated_content.get("summary", []))
                

                


    
    return render_template("dashboard.html",
        user=current_user,
        total_income=total_income,
        incomes=incomes,
        total_expense=total_expense,
        expenses=expenses,
        Balance_amount=Balance_amount,
        recent_transactions=recent_transactions,
        btn_clicked=btn_clicked,
        savings=savings,
        completion_percentage=completion_percentage,
        total_saving=total_saving,
        status=status,
        score=score,
        category_breakdown=category_breakdown,
        summary_health=summary_health,
        highest_category=highest_category,
        highest_category_amount=highest_category_amount,
        Goal_name=Goal_name,
        Target_amount=Target_amount,
        Current_amount=Current_amount,
        Goal_status=Goal_status,
        observation=observation,
        recommendation=recommendation,
        summary_ai=summary_ai,
        error=error
    )
