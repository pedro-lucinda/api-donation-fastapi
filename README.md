# in progress

### Run the application
```
  uvicorn app.main:app --reload
```

### Migrations
- Make migration
```
alembic revision -m "name"
```

- Migrate
```
  alembic upgrade head
```

### Dependencies
- Add new dependencies to requirements.in
- Update requirements.txt
```
pip-compile requirements.in
```

- Update the dep to latest version
```
pip-compile --upgrade
```
