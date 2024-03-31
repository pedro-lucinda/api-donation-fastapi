#!/bin/bash

# Navigate to the project root directory if the script is run from another directory
cd "$(dirname "$0")"/../

echo "Formatting and linting code..."

# Format code with black
echo "Running black..."
black ./app --line-length=80

# Sort imports with isort
echo "Running isort..."
isort ./app --profile black

# Lint code with pylint, ignoring the alembic directory
echo "Running pylint..."
pylint --rcfile=.pylintrc --ignore=alembic/ ./app

echo "Code formatting and linting completed."
