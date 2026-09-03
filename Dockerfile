FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE ${PORT}

# Run the unified FastAPI server
# Using uvicorn directly as it handles the single-process deployment efficiently for this demo
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT}
