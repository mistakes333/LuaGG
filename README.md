# website
Online login System
Video Guide
https://youtu.be/7uwpOhNKIjg


openssl genrsa -out private.key 2048

openssl req -new -key private.key -out certificate.csr


export FLASK_RUN_PORT=443

flask run


git@github.com:mistakes0fficial/LuaGG.git
