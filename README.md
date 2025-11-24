# Clothing Sales Record

A minimal Python project that combines a Flask back end with a templated front end for tracking clothing sales records. Data is stored in a local SQLite database and presented in a responsive dashboard.

## Features
- Add sales with item details, size, category, quantity, price, and date.
- View recent sales in a table with per-row totals.
- See summary metrics for total revenue, items sold, and average price.
- Export data or summary via JSON endpoints.

## Project layout
- `backend/` — Flask app, SQLAlchemy models, and database setup.
- `frontend/` — HTML template and CSS served by Flask.
- `requirements.txt` — dependencies to install.

## Getting started
1. Create and activate a Python 3 virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python -m backend.app
   ```
4. Open http://localhost:5000 to add and review sales.

Database files are created under `instance/` automatically.
