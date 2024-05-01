# FastAPI Application

## Overview
Brief description of your application, its purpose, and functionality.

## Features
- User Authentication
- Database integration with SQLAlchemy
- Asynchronous requests handling
- Docker support for containerization

## Installation
```bash
git clone <repository-url>
cd <repository-name>
pip install -r requirements.txt
```

## Running the application
```bash
uvicorn app.main:app --reload
```


### Run the application
```bash
  uvicorn app.main:app --reload
```

### Making Database Migrations
To create new database migrations after model changes:
```base
alembic revision -m "name"
```

- To apply migrations to the database:
```base
  alembic upgrade head
```


## Development Tools
We have included scripts to help with linting, formatting, and database migrations.

### Formatting
To format the codebase, run:
```bash
sh scripts/format.sh
```

### Linting
To lint the codebase, run:
```bash
sh scripts/lint.sh
```

## Managing Dependencies

### Adding New Dependencies
To add a new dependency to the project:

1. Add the package to `requirements.in` with the desired version.
2. Run the following command to update `requirements.txt`:
    ```bash
    pip-compile requirements.in
    ```

This will generate a `requirements.txt` with all the necessary sub-dependencies pinned to the latest versions that are compatible with your direct dependencies.

### Updating Dependencies
To update all packages to their latest permissible versions, you can use the `-U` option:

```bash
pip-compile -U requirements.in
