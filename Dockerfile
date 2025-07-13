# Base image
FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y build-essential git && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

# Default command
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
