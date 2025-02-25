# Use the official Python 3.11 Alpine image
FROM python:3.11-alpine

# Set the working directory
WORKDIR /app

# Install system dependencies required for Poetry and dependencies that need to be built
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev python3-dev

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy only the dependency files first to take advantage of Docker's cache
COPY pyproject.toml poetry.lock ./

# Install project dependencies without creating a virtual environment inside the container
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the code to the container
COPY . .

# Set the container startup command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
