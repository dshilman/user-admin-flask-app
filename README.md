# Use Admin App

## Installation Instructions

### Installation

Pull down the source code from this GitLab repository:

```cmd
git clone https://github.com/dshilman/user-admin-flask-app.git
```

Create a new virtual environment:

```cmd
cd user-admin-flask-app
python3 -m venv venv
```

Activate the virtual environment:

```cmd
.\venv\scripts\activate
```

Install the python packages specified in requirements.txt:

```cmd
(venv) cd code
(venv) pip install -r requirements.txt
```

Run app on Linux
```shell
(venv) gunicorn --workers=2 --log-level=info app:app
```

Run app on Windows
```cmd
(venv) flask --app app --debug run
```

SQLite DDL Commands
```cmd
(venv)$ flask shell
>>> from modules import database
>>> database.drop_all()
>>> database.create_all()
>>> quit()
```

##Flask CLI

Run Flask App
```cmd
(venv)$ flask --app app --debug run
```

Flask Version
```cmd
(venv)$ flask --version
```

Flask Routes
```cmd
(venv)$ flask routes
```
or
```cmd
(venv)$ flask shell
>>> print(app.url_map)

```

DB Creation
```cmd
(venv)$ flask shell

>>> from modules import database
>>> database.drop_all()
>>> database.create_all()
>>> database.metadata.tables.keys() 
>>> database.session.commit()
>>> quit()
```

DB Migration
```cmd
$ flask db init
$ flask db revision --autogenerate -m "<descriptive message>"
$ flask db upgrade head
```

Access SQLLite via sqlite cli
```cmd
sqlite3 instance\app.db
.schema firms
.schema users
```
