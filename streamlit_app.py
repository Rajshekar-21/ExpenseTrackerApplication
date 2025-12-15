import streamlit as st
from datetime import date

from database import init_db
from services import (
    add_expense,
    set_budget,
    get_monthly_spending,
    check_budget_alerts,
    add_shared_expense,
    calculate_split,
    get_total_expenses,
    get_total_categories,
    get_total_shared_expenses,
    get_remaining_budgets,
)

def main():
    # Make sure tables exist
    init_db()

    st.title("💰 Expense Tracker Web App")

    # Sidebar Navigation
    menu = st.sidebar.selectbox(
        "Navigation",
        [
            "Dashboard",
            "Add Expense",
            "Set Monthly Budget",
            "View Monthly Spending",
            "View Alerts",
            "Add Shared Expense",
            "View Group Split",
        ],
    )

    # ---------------------------------------------------------
    # -------------------- DASHBOARD ---------------------------
    # ---------------------------------------------------------
    if menu == "Dashboard":
        st.title("📊 Dashboard Overview")

        total_exp = get_total_expenses()
        total_cat = get_total_categories()
        total_shared = get_total_shared_expenses()

        # Metric Cards
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total Expenses", f"₹{total_exp:.2f}")
        col2.metric("📂 Total Categories", total_cat)
        col3.metric("👥 Shared Expenses", total_shared)

        st.write("---")
        st.subheader("📉 Remaining Budgets")

        month_input = st.date_input("Select Month", value=date.today())
        month_str = month_input.strftime("%Y-%m")

        remaining = get_remaining_budgets(month_str)

        if not remaining:
            st.info("No budgets found for this month.")
        else:
            for category, budget_amt, spent, rem in remaining:
                st.write(f"### 📌 {category}")

                if budget_amt > 0:
                    st.progress(max(0, min(1, spent / budget_amt)))
                else:
                    st.warning("No budget set for this category.")

                st.write(f"**Budget:** ₹{budget_amt}")
                st.write(f"**Spent:** ₹{spent}")
                st.write(f"**Remaining:** ₹{rem}")
                st.write("---")

    # ---------------------------------------------------------
    # -------------------- ADD EXPENSE -------------------------
    # ---------------------------------------------------------
    elif menu == "Add Expense":
        st.header("➕ Add Expense")

        with st.form("add_expense_form"):
            user = st.text_input("User name")
            category = st.text_input("Category (e.g., Food, Travel, Shopping)")
            amount = st.number_input("Amount", min_value=0.0, format="%.2f")
            expense_date = st.date_input("Date", value=date.today())

            submitted = st.form_submit_button("Save Expense")

            if submitted:
                if not user or not category or amount <= 0:
                    st.error("Please fill all fields correctly.")
                else:
                    date_str = expense_date.strftime("%Y-%m-%d")
                    msg = add_expense(amount, category, date_str, user)
                    st.success(msg)

    # ---------------------------------------------------------
    # -------------------- SET BUDGET --------------------------
    # ---------------------------------------------------------
    elif menu == "Set Monthly Budget":
        st.header("📅 Set Monthly Budget")

        with st.form("set_budget_form"):
            user = st.text_input("User name")
            category = st.text_input("Category")
            month_date = st.date_input(
                "Month (pick any day in the month)", value=date.today()
            )
            budget_amount = st.number_input(
                "Budget Amount", min_value=0.0, format="%.2f"
            )

            submitted = st.form_submit_button("Save Budget")

            if submitted:
                if not user or not category or budget_amount <= 0:
                    st.error("Please fill all fields correctly.")
                else:
                    month_str = month_date.strftime("%Y-%m")
                    msg = set_budget(category, month_str, budget_amount, user)
                    st.success(msg)

    # ---------------------------------------------------------
    # -------------------- VIEW SPENDING ------------------------
    # ---------------------------------------------------------
    elif menu == "View Monthly Spending":
        st.header("📊 View Monthly Spending")

        user = st.text_input("User name")
        month_date = st.date_input(
            "Month (pick any day in the month)", value=date.today()
        )

        if st.button("Show Spending"):
            if not user:
                st.error("Please enter user name.")
            else:
                month_str = month_date.strftime("%Y-%m")
                total = get_monthly_spending(user, month_str)
                st.info(
                    f"Total spending for {user} in {month_str}: ₹{total:.2f}"
                )

    # ---------------------------------------------------------
    # -------------------- VIEW ALERTS --------------------------
    # ---------------------------------------------------------
    elif menu == "View Alerts":
        st.header("⚠️ Budget Alerts")

        user = st.text_input("User name")
        month_date = st.date_input(
            "Month (pick any day in the month)", value=date.today()
        )
        user_email = st.text_input("Email (optional for email alerts)")

        if st.button("Check Alerts"):
            if not user:
                st.error("Please enter user name.")
            else:
                month_str = month_date.strftime("%Y-%m")
                alerts = check_budget_alerts(
                    user, month_str, user_email if user_email else None
                )

                if not alerts:
                    st.success("No alerts. You are within your budgets. ✅")
                else:
                    for a in alerts:
                        st.warning(a)

    # ---------------------------------------------------------
    # ------------------ ADD SHARED EXPENSE --------------------
    # ---------------------------------------------------------
    elif menu == "Add Shared Expense":
        st.header("👥 Add Shared Expense (Splitwise-like)")

        with st.form("shared_expense_form"):
            group_name = st.text_input("Group Name")
            description = st.text_input("Description (e.g., Dinner, Trip)")
            total_amount = st.number_input(
                "Total Amount", min_value=0.0, format="%.2f"
            )
            payer = st.text_input("Paid by (user name)")
            members_text = st.text_input(
                "Members (comma separated, e.g., Raj,Sid,Sam)"
            )

            submitted = st.form_submit_button("Save Shared Expense")

            if submitted:
                if (
                    not group_name
                    or not description
                    or not payer
                    or not members_text
                    or total_amount <= 0
                ):
                    st.error("Please fill all fields correctly.")
                else:
                    members = [
                        m.strip() for m in members_text.split(",") if m.strip()
                    ]
                    if len(members) == 0:
                        st.error("Please provide at least one member.")
                    else:
                        msg = add_shared_expense(
                            group_name, description, total_amount, payer, members
                        )
                        st.success(msg)

    # ---------------------------------------------------------
    # -------------------- VIEW SPLIT ---------------------------
    # ---------------------------------------------------------
    elif menu == "View Group Split":
        st.header("📉 View Group Split")

        group_name = st.text_input("Group Name")

        if st.button("Calculate Split"):
            if not group_name:
                st.error("Please enter group name.")
            else:
                result = calculate_split(group_name)
                if not result:
                    st.info("No shared expenses found for this group.")
                else:
                    st.subheader("Who owes how much:")
                    for member, balance in result.items():
                        if balance < 0:
                            st.write(
                                f"✅ {member} should RECEIVE ₹{abs(balance):.2f}"
                            )
                        else:
                            st.write(
                                f"💸 {member} should PAY ₹{balance:.2f}"
                            )


# Run App
if __name__ == "__main__":
    main()
