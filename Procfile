web: gunicorn -b 0.0.0.0 -p 80 app:app
ssl: gunicorn -b 0.0.0.0 -p 443 gunicorn --certfile=server.crt --keyfile=server.key -w 4 app:app
