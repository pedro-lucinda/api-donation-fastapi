# in progress

### Migrations
```
- Make migration
alembic revision -m "name"

```

- Migrate
```
  alembic upgrade head
```


### Run the application
```
  uvicorn app.main:app --reload

```