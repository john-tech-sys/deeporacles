FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "deeporacles.wsgi:application"]
