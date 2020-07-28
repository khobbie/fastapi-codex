# fastapi-codex
* Local Apache Server like [XAMPP]([https://www.apachefriends.org/download.html])
* Install [Python 3.6+]([https://www.python.org/])
* Install packages `pip3 install -r requirements.txt`
* Import ```db/codex_db.sql``` into local Sever Database

### Run uvicorn serve

```
uvicorn main:app --reload
```

### Documentation [Swagger Docs]([http://127.0.0.1:8000/docs])
```
http://127.0.0.1:8000/docs
```
### Documentation [Redocs Docs]([http://127.0.0.1:8000/redocs])
```
http://127.0.0.1:8000/redocs
```