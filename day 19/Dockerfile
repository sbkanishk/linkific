# 1. Use an official lightweight Python image
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Install dependencies directly into the container
RUN pip install --no-cache-dir fastapi uvicorn redis pydantic

# 5. Copy the rest of your local day 19 files into the container
COPY . /app/

# (The startup command is handled in our docker-compose file!)