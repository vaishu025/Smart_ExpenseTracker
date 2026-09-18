# Smart Expense Tracker using Django

A complete, ready-to-run **Smart Expense Tracker** web application built with Django. Users can register, log in, add expenses (with automatic keyword-based category prediction), edit/delete their records, filter by date range, view Plotly visualizations, and export their data as CSV or PDF — with each user's data fully isolated from every other user.

---

## Features

- Secure registration, login, and logout (Django's built-in authentication)
- Add / view / edit / delete expenses (full CRUD)
- Automatic expense category prediction from the description (simple keyword matching — no ML)
- Filter expenses by **Today**, **This Week**, **This Month**, or **All**
- Dashboard with summary cards (Total, Today, This Week, This Month)
- Analytics page with a **Plotly** category pie/donut chart and a spending-over-time line chart
- Download expenses as **CSV**
- Download a formatted **PDF report** (built with ReportLab)
- Per-user data isolation — no user can ever see, edit, delete, or download another user's expenses
- Django Admin panel for managing all expenses
- Responsive Bootstrap 5 UI that works on desktop and mobile

## Technology Stack

- **Backend:** Python 3, Django, Django built-in authentication, SQLite
- **Frontend:** HTML5, CSS3, Bootstrap 5, Django Templates, Bootstrap Icons
- **Visualization:** Plotly / Plotly.js
- **Export:** Python `csv` module, ReportLab (PDF)

---

## Project Structure

```text
smart_expense_tracker/
│
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
│
├── smart_expense_tracker/       # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── expenses/                    # Main app
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── category_predictor.py    # Keyword-based category prediction
│   ├── utils.py                 # Date filters, CSV & PDF export helpers
│   ├── migrations/
│   └── templates/expenses/      # Dashboard, add/edit forms, analytics, etc.
│
├── templates/
│   ├── base.html                # Shared layout + navbar
│   └── registration/
│       ├── login.html
│       └── register.html
│
└── static/
    ├── css/style.css
    └── js/main.js
```

---

## How to Run the Project in VS Code (Windows)

### Step 1 – Extract the ZIP
Extract the downloaded ZIP file to a folder of your choice, e.g. `C:\Projects\smart_expense_tracker`.

### Step 2 – Open the project in VS Code
Open VS Code → **File → Open Folder** → select the extracted `smart_expense_tracker` folder.

### Step 3 – Create a virtual environment
Open a terminal in VS Code (`` Ctrl+` ``) and run:

```bash
python -m venv venv
```

### Step 4 – Activate the virtual environment

**Windows PowerShell:**
```bash
venv\Scripts\Activate.ps1
```

If PowerShell blocks the script (execution policy error), either run PowerShell as Administrator once and execute:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
or simply use **Command Prompt** instead:
```bash
venv\Scripts\activate
```

You should see `(venv)` appear at the start of your terminal prompt once activated.

### Step 5 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 6 – Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7 – Create an admin (superuser) account
```bash
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### Step 8 – Run the development server
```bash
python manage.py runserver
```

### Step 9 – Open the app in your browser
Visit:
```text
http://127.0.0.1:8000/
```

You'll be redirected to the login page. Click **Register** to create a new account, or use `/register/` directly.

### Accessing Django Admin
```text
http://127.0.0.1:8000/admin/
```
Log in with the superuser credentials created in Step 7. From here you can view, search, filter, edit, and delete any user's expense records.

---

## Quick Command Reference

After extracting the ZIP, from inside the project folder:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in your browser.

---

## How Category Prediction Works

`expenses/category_predictor.py` contains a simple dictionary (`CATEGORY_KEYWORDS`) mapping each category to a list of common keywords (e.g. "uber", "pizza", "electricity"). When you type an expense description on the **Add Expense** page, the app checks the description (case-insensitively) against these keywords and pre-selects the matching category. If nothing matches, it defaults to **Other**. You can always change the predicted category manually before saving.

Example predictions:

| Description         | Predicted Category |
|----------------------|--------------------|
| Uber to college      | Travel             |
| Pizza and burger     | Food               |
| Bought a new shirt   | Shopping           |
| Electricity bill     | Bills              |
| Movie ticket         | Entertainment      |

---

## Notes

- This project uses **SQLite**, so no external database setup is required — `db.sqlite3` is created automatically when you run migrations.
- All amounts are validated to be greater than zero.
- Every expense-related page requires login (`@login_required`), and every query is filtered by `user=request.user`, so users can never access each other's data — even if they guess another user's expense ID directly in the URL (it returns a 404).
- `DEBUG = True` is set for local development/demo purposes. If you ever deploy this project publicly, set `DEBUG = False` and configure `ALLOWED_HOSTS` and a proper `SECRET_KEY` before doing so.

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'django'`** → Make sure your virtual environment is activated (`(venv)` should show in the terminal) and that you ran `pip install -r requirements.txt`.
- **PowerShell won't activate the venv** → Use `venv\Scripts\activate` in Command Prompt instead, or run the `Set-ExecutionPolicy` command from Step 4.
- **Port already in use** → Run `python manage.py runserver 8080` and open `http://127.0.0.1:8080/` instead.
- **Static files (CSS/JS) not loading** → Make sure `DEBUG = True` in `settings.py` during local development (already set by default in this project).

---

Built as a Django mini-project — **Smart Expense Tracker**.
