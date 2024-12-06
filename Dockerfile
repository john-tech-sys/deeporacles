FROM python:3.12-slim

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    build-essential \
    libffi-dev \
    libssl-dev

# Set the working directory
WORKDIR /app

# Copy the project files to the working directory
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["gunicorn", "deeporacles.wsgi:application"]
]
