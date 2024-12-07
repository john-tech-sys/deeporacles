release: python3 manage.py migrate
web: gunicorn deeporacles.wsgi:application --bind 0.0.0.0:8000 --log-file -
