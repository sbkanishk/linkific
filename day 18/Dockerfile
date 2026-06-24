# 1. Base image (Python 3.11 optimized for size)
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy requirements and install them
# (We do this before copying the rest of the code to leverage layer caching!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of your application code
COPY . .

# 5. Expose the port FastAPI runs on
EXPOSE 8000

# 6. Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]