FROM python:3.12-slim

# RUN apt-get update && apt-get install -y gcc
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    build-essential && \
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "deeporacles.wsgi:application"]
