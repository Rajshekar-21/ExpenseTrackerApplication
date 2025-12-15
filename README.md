Python 3.13 compatible Expense Tracker using sqlite3.


# 💰 Expense Tracker – Budgeting & Shared Expense Management


## 📌 **1. Project Overview**

This project is a feature-rich **expense tracking system** that helps users:

* Add daily expenses
* Set monthly budgets
* Receive alerts when budgets are exceeded
* View monthly spending
* Manage shared/group expenses
* View a clean dashboard with totals, categories, remaining budgets

The application comes with both:

* **CLI version** (`app.py`)
* **Web UI version** (`streamlit_app.py`)

---

## 🛠️ **2. Tech Stack**

| Component           | Technology                |
| ------------------- | ------------------------- |
| Backend Logic       | Python                    |
| Database            | SQLite                    |
| Web UI              | Streamlit                 |
| Notification System | Optional Email (SMTP/API) |
| Data handling       | pandas                    |

---

## 📁 **3. Project Structure**

```
│── app.py                # CLI interface
│── streamlit_app.py      # Web dashboard (UI)
│── services.py           # Business logic
│── database.py           # All DB operations + table creation
│── email_service.py      # Email sending wrapper
│── email_config.py       # Email configuration (API/SMTP credentials)
│── expenses.db           # SQLite database (auto-created)
│── cli.py                # Utility CLI handlers
│── README.md             # This file
```

---

## ✅ **4. Features Implemented**

### ✔ Expense Management

* Add expenses (user, category, amount, date)
* View monthly totals

### ✔ Budget Tracking

* Set monthly category budgets
* Dashboard display of spent vs budget
* Alerts when spending exceeds the budget

### ✔ Shared Expenses

* Add group expenses (Splitwise style)
* Automatic split calculation
* Shows how much each member pays/owes

### ✔ Dashboard

* Total expenses
* Total categories
* Shared expenses count
* Remaining budgets visualized

### ✔ Optional Email Alerts

If configured, the app sends an email when a user exceeds their monthly budget.

---

## 📦 **5. Installation & Setup**

### **Step 0 — Prerequisites**

* Python 3.10 or above
* Git

---

## **Step 1 — Clone the Repository**

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

---

## **Step 2 — Create Virtual Environment**

### Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

---

## **Step 3 — Install Required Packages**

Create a **requirements.txt** file:

```
streamlit==1.32.2
pandas==2.2.1
requests==2.31.0
python-dateutil==2.9.0.post0
```

Install:

```bash
pip install -r requirements.txt
```

---

## **Step 4 — Database Setup**

No manual setup needed.

The database **expenses.db** is automatically created when the app runs.

If you want a fresh start, delete:

```
expenses.db
```

---

# 🚀 **6. Running the Application**

---

## ▶ **Option A — Run CLI Application**

```bash
python app.py
```

Sample menu:

```
===== Expense Tracker =====
1. Add Expense
2. Set Monthly Budget
3. View Monthly Spending
4. Check Alerts
5. Add Shared Expense
6. View Group Split
0. Exit
```

---

## ▶ **Option B — Run Web UI (Streamlit Dashboard)**

```bash
streamlit run streamlit_app.py
```

or

```bash
python -m streamlit run streamlit_app.py
```

It will open automatically in browser:

```
http://localhost:8501
```

---

# 📧 **7. Email Notification Setup (Optional)**

Email alerts work ONLY if the evaluator configures credentials in:

```
email_config.py
```

Supported providers:

* MailerSend
* SMTP2GO
* Any SMTP service

If not configured → alerts still show inside the UI (no errors).

---

# 🧪 **8. Test Cases (From PDF Requirements)**

### **Test Case 1 – Add Expense**

| Input    | Value      |
| -------- | ---------- |
| User     | Raj        |
| Category | Food       |
| Amount   | 120        |
| Date     | 2025-01-05 |

**Expected Output:**

```
Expense added successfully!
```

---

### **Test Case 2 – Monthly Spending**

| User | Raj |
| Month | 2025-01 |

**Expected Output:**

```
Total spending for Raj in 2025-01: ₹120.00
```

---

### **Test Case 3 – Add Budget**

| User | Raj |
| Category | Food |
| Month | 2025-01 |
| Budget | 1000 |

**Expected Output:**

```
Budget set successfully!
```

---

### **Test Case 4 – Remaining Budget Dashboard**

After adding expenses:

* Budget: 1000
* Spent: 120

**Expected Output in UI:**

```
Remaining: ₹880
Progress bar < 20%
```

---

### **Test Case 5 – Budget Exceeded**

| Expenses | 1120 |
| Budget | 1000 |

**Expected Output:**

```
Budget exceeded for Food! You spent 1120 out of 1000.
```

---

### **Test Case 6 – Email Sent (Optional)**

| User | Raj |
| Email | [raj@gmail.com](mailto:raj@gmail.com) |

**Expected Terminal Output:**

```
['Budget exceeded for Food! You spent 1120 out of 1000.']
Email notification sent.
```

**Email Content:**

```
Subject: Budget Exceeded Alert
Body: Budget exceeded for Food! You spent 1120 out of 1000.
```

---

### **Test Case 7 – Shared Expense Split**

| Group Name | Trip |
| Total Amount | 3000 |
| Paid By | Raj |
| Members | Raj, Sid, Sam |

**Expected Output:**

```
Raj should receive ₹2000
Sid should pay ₹1000
Sam should pay ₹1000
```

---

# 🗂 **9. How to Check Stored Data**

Open Python:

```bash
python
```

Run:

```python
import sqlite3
conn = sqlite3.connect("expenses.db")
cur = conn.cursor()
cur.execute("SELECT * FROM expenses")
print(cur.fetchall())
conn.close()
```

---


