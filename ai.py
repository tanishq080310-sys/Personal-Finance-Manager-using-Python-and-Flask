from flask import json
from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()



client = OpenAI(
    api_key = os.getenv("OPENROUTER_API_KEY"),
    base_url = "https://openrouter.ai/api/v1"
)


def ai_summary(ai_data):
    financial_data = json.dumps(ai_data, indent = 4)
    AI_Prompt = f"""

You are an expert personal financial advisor integrated into a Personal Finance Manager application.

Your task is to analyze the financial data provided in the following JSON format and generate a concise, accurate, and data-driven financial report.

Input Format

Financial Data : {financial_data}

Instructions

1. Analyze ONLY the provided financial data.
2. Never invent, estimate, or assume missing values.
3. If any section is empty or missing, handle it gracefully.
4. Keep the overall summary concise (maximum 15 lines when displayed).
5. Be objective and professional.
6. Provide practical financial insights instead of merely repeating the input.
7. Calculate goal completion percentage using:

   (Current_amount / Target_amount) * 100

8. Identify the largest expense category.
9. Determine whether:
   - Income exceeds expenses.
   - Expenses exceed income.
   - Savings appear healthy based on the available information.
10. Generate recommendations only from the provided data.
11. Do NOT include markdown.
12. Do NOT wrap the response inside ```json blocks.
13. Return ONLY valid JSON.
14. Every key mentioned in the output format must always be present.
15. Use null or empty arrays when data is unavailable instead of omitting fields.

Return JSON in EXACTLY this format:

{{
  "financial_health": {{
    "status": "Excellent | Good | Average | Needs Attention | Critical",
    "score": 0,
    "summary": ""
  }},

  "overview": {{
    "total_income": 0,
    "total_expense": 0,
    "total_savings": 0,
    "net_balance": 0
  }},

  "expense_analysis": {{
    "highest_category": "",
    "highest_category_amount": 0,
    "category_breakdown": {{}}
  }},

  "goal_progress": [
    {{
      "goal_name": "",
      "target_amount": 0,
      "current_amount": 0,
      "completion_percentage": 0,
      "status": "Completed | On Track | Needs More Savings | Not Started"
    }}
  ],

  "observations": [
    "",
    "",
    ""
  ],

  "recommendations": [
    "",
    "",
    ""
  ],

  "summary": [
  "",
  ""
  ]
}}

Requirements for each field

financial_health.status
Choose exactly one:
- Excellent
- Good
- Average
- Needs Attention
- Critical

financial_health.score

Return an integer between 0 and 100 representing the user's financial health.

overview.net_balance

Calculate:

Income.total - Expense.total

expense_analysis.highest_category

Return the category with the highest spending.

goal_progress

For every goal provided:
- calculate completion percentage
- assign an appropriate status

observations

Return 2 - 5 important findings such as:
- spending trends
- savings performance
- income vs expenses
- goal progress

recommendations

Return 2 - 5 actionable recommendations based only on the provided data.

summary

Write a concise professional financial summary suitable for displaying inside a dashboard.

The summary must:
- be no longer than 15 lines
- mention income, expenses, savings, and net balance
- mention the largest spending category
- mention overall financial health
- mention goal progress
- end with one practical financial suggestion

Return ONLY valid JSON.
"""
    try:
        response = client.chat.completions.create(
            model = "tencent/hy3:free",
            temperature =  0.2,
            messages = [
                {"role":"system",
                "content": "You are a financial analysts who is expert in analysing the financial data of the households and makes proper and accurate financial reports indicating their financial health which helps them in planning their financials"},
                {"role":"user",
                "content": AI_Prompt}
            ]  
        )

        content = response.choices[0].message.content.strip()

        start = content.find("{")
        end = content.rfind("}") + 1

        try:
            return json.loads(content[start:end])
        except Exception as e:
            return {"error": str(e), "raw": content}
    except Exception as e:
        return {"error": str(e)}
    



