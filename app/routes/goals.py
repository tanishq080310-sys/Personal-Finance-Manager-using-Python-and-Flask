from flask import redirect, render_template, request,Blueprint
from flask_login import login_required, current_user
from models import db, Goals, Savings


goals_bp = Blueprint("goals",__name__)



@goals_bp.route("/goals",methods = ["GET","POST"])
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

