from database import get_connection
from email_service import send_email

def add_expense(amount, category, date, user):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (amount, category, date, user) VALUES (?, ?, ?, ?)",
                (amount, category, date, user))
    conn.commit()
    conn.close()
    return "Expense added."

def set_budget(category, month, amount, user):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO budgets (category, month, amount, user) VALUES (?, ?, ?, ?)",
                (category, month, amount, user))
    conn.commit()
    conn.close()
    return "Budget set."

def get_monthly_spending(user, month):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM expenses WHERE user=? AND date LIKE ?", (user, f"{month}-%"))
    total = cur.fetchone()[0] or 0
    conn.close()
    return total

def check_budget_alerts(user, month, user_email=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT category, amount FROM budgets WHERE user=? AND month=?", (user, month))
    budgets = cur.fetchall()

    cur.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user=? AND date LIKE ? GROUP BY category",
        (user, f"{month}-%")
    )
    expenses = dict(cur.fetchall())

    conn.close()

    alerts = []
    for category, budget_amount in budgets:
        spent = expenses.get(category, 0)

        if spent > budget_amount:
            msg = f"Budget exceeded for {category}! You spent {spent} out of {budget_amount}."
            alerts.append(msg)

            if user_email:
                send_email(user_email, "Budget Exceeded Alert", msg)

        elif spent > 0.9 * budget_amount:
            msg = f"Warning: Only 10% of your {category} budget is left."
            alerts.append(msg)

            if user_email:
                send_email(user_email, "Budget Warning Alert", msg)

    return alerts

def add_shared_expense(group_name, description, amount, payer, members):
    conn = get_connection()
    cur = conn.cursor()
    members_str = ",".join(members)
    cur.execute(
        "INSERT INTO shared_expenses (group_name, description, total_amount, payer, members) "
        "VALUES (?, ?, ?, ?, ?)",
        (group_name, description, amount, payer, members_str)
    )
    conn.commit()
    conn.close()
    return "Shared expense recorded."

def calculate_split(group_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT description, total_amount, payer, members FROM shared_expenses WHERE group_name=?",
        (group_name,)
    )
    rows = cur.fetchall()
    conn.close()

    result = {}
    for desc, total, payer, members_str in rows:
        members = members_str.split(",")
        per_head = total / len(members)
        for m in members:
            result[m] = result.get(m, 0) + per_head
        result[payer] -= total
    return result
def get_total_expenses():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT SUM(amount) FROM expenses")
    total = cur.fetchone()[0] or 0

    conn.close()
    return total


def get_total_categories():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(DISTINCT category) FROM expenses")
    total = cur.fetchone()[0] or 0

    conn.close()
    return total


def get_total_shared_expenses():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM shared_expenses")
    total = cur.fetchone()[0] or 0

    conn.close()
    return total


def get_remaining_budgets(month):
    conn = get_connection()
    cur = conn.cursor()

    # fetch budgets
    cur.execute("SELECT category, amount, user FROM budgets WHERE month=?", (month,))
    budgets = cur.fetchall()

    # fetch expenses by category
    cur.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE date LIKE ?
        GROUP BY category
    """, (f"{month}-%",))
    expenses = dict(cur.fetchall())

    conn.close()

    remaining = []
    for category, budget_amount, user in budgets:
        spent = expenses.get(category, 0)
        rem = budget_amount - spent
        remaining.append((category, budget_amount, spent, rem))

    return remaining
