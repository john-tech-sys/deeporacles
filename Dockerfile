# Use a Python base image
FROM python:3.12

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . /app

# Start the Gunicorn server
# CMD ["gunicorn", "--workers=1", "--threads=2", "--timeout=60", "deeporacles.wsgi:application"]
CMD ["gunicorn", "--workers=1", "--threads=2", "--timeout=60", "--bind", "0.0.0.0:8000", "--log-file", "-", "deeporacles.wsgi:application"]
