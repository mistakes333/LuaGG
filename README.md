# website
Online login System
Video Guide
https://youtu.be/7uwpOhNKIjg


openssl genrsa -out key.pem 2048

openssl req -new -x509 -key key.pem -out certificate.pem -days 365


export FLASK_RUN_PORT=443

flask run --cert=adhoc


git@github.com:mistakes0fficial/LuaGG.git
