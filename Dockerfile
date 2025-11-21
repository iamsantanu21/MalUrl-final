# Use a slim Python image
FROM python:3.11-slim

# Avoid Python writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# System dependencies (for numpy, pandas etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /app/

# Cloud Run expects the app to listen on PORT env (default 8080)
ENV PORT=8080

# Expose port (for local testing; Cloud Run does its own routing)
EXPOSE 8080

# Start FastAPI using uvicorn
CMD ["uvicorn", "server-updated:app", "--host", "0.0.0.0", "--port", "8080"]
