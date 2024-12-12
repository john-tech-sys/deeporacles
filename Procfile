release: python3 manage.py migrate && python3 manage.py collectstatic --noinput

web: gunicorn deeporacles.wsgi