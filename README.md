
# User Admin Flask App

A lightweight Flask-based user administration application supporting development and production modes, SQLite database creation and migrations, and convenient Flask CLI utilities.

## Installation
```bash
git clone https://github.com/dshilman/user-admin-flask-app.git
cd user-admin-flask-app
python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
cd code
pip install -r requirements.txt
```

## Running the Application
### Windows
```bash
flask --app app --debug run
```
### Linux
```bash
gunicorn --workers=2 --log-level=info app:app
```

## Database Commands (SQLite)
```bash
flask shell
>>> from modules import database
>>> database.drop_all()
>>> database.create_all()
>>> quit()
```

## Flask Utilities
```bash
flask routes
flask --version
```

## Database Migration
```bash
flask db init
flask db revision --autogenerate -m "message"
flask db upgrade head
```

## Access SQLite DB
```bash
sqlite3 instance/app.db
.schema
```

