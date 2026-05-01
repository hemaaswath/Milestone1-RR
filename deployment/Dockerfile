FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway sets this via environment variable)
EXPOSE $PORT

# Use gunicorn for production
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
