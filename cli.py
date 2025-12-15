from database import init_db
from services import *

def menu():
    print("\n===== Expense Tracker =====")
    print("1. Add Expense")
    print("2. Set Monthly Budget")
    print("3. View Monthly Spending")
    print("4. Check Alerts")
    print("5. Add Shared Expense")
    print("6. View Group Split")
    print("0. Exit")
    return input("Enter choice: ")

def main():
    init_db()

    while True:
        choice = menu()

        if choice == "1":
            amt=float(input("Amount: "))
            cat=input("Category: ")
            date=input("Date (YYYY-MM-DD): ")
            user=input("User: ")
            print(add_expense(amt, cat, date, user))

        elif choice == "2":
            cat=input("Category: ")
            month=input("Month (YYYY-MM): ")
            amt=float(input("Budget Amount: "))
            user=input("User: ")
            print(set_budget(cat, month, amt, user))

        elif choice == "3":
            month=input("Month (YYYY-MM): ")
            user=input("User: ")
            print("Total Spending:", get_monthly_spending(user, month))

        elif choice == "4":
            month = input("Month (YYYY-MM): ")
            user = input("User: ")
            user_email = input("Enter your email to receive alerts: ")
            print(check_budget_alerts(user, month, user_email))

        elif choice == "5":
            group=input("Group name: ")
            desc=input("Description: ")
            amt=float(input("Total amount: "))
            payer=input("Paid by: ")
            members=input("Members (comma separated): ").split(",")
            print(add_shared_expense(group, desc, amt, payer, members))

        elif choice == "6":
            group=input("Group name: ")
            print(calculate_split(group))

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")
