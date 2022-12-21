from flask import *
try:
 from dateutil import parser
 from datetime import datetime, date, timedelta
except:
 os.system('python3 -m pip install --user python-dateutil==2.8.2')
 os.system('python3 -m pip install --user Flask==2.1.2')

import os, random, string, subprocess, traceback, sockets, ssl, request, sqlite3, smtplib, json, session


keyurl = "http://13.58.115.54:8000/nwkey"
name = "MT"

app = Flask(__name__)



def getip():
   if request.headers.getlist("X-Forwarded-For"):
      ip = request.headers.getlist("X-Forwarded-For")[0]
   else:
      ip = request.remote_addr
   return str(ip)


def checkkey(ip_or_key, **args):
    ip = key = date =  None
    nokey = args.get("ip", True)
    if os.path.exists('keys.txt'):
     with open('keys.txt') as f:
         lines = f.read().splitlines()
     for i in lines:
        if i == "":
             continue
        x1 = i.split(";")
        if x1[0] == ip_or_key or (nokey and x1[1] == ip_or_key):
            key = x1[0]
            ip = x1[1]
            date = x1[2]
            break
    return key,ip,date


def clearr():
 try:
   to = 0
   if os.path.exists('keys.txt'):
      datenow = datetime.now()
      with open('keys.txt') as f:
         lines = f.read().splitlines()
      for i in lines:
          if i == "":
             continue
          x = i.split(';')
          date = parser.parse(x[2])
          if int((datenow - date).days) > 0:
             os.system(f"sed -i '/{i}/d' keys.txt")
             to = to + 1
      os.system("sed -i '/^$/d' keys.txt")
   return to
 except Exception as e:
     return str(e)

def makepass(length):
    letters = string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def createkey():
    myip = getip()
    key = name+makepass(20)
    date = str(datetime.now())
    if os.path.exists('keys.txt'):
        m = "a"
    else:
        m = "w"
    with open("keys.txt", m) as a_file:
         a_file.write(f"\n{key};{myip};{date}")
    return key,myip,date


def getexpire(days,seconds):
   hours = 23-(days * 24 + seconds // 3600)
   minutes = 60-((seconds % 3600) // 60)
   seconds = 60-(seconds % 60)
   return hours, minutes, seconds



@app.route('/')
def hello_world():
    xx = request.cookies.get('ip')
    clearr()
    rrip = myip = getip()
    if not os.path.exists('admin.txt'):
      with open('admin.txt','a') as f:
          pass
    tedd = ""
    if xx:
       key,oip,date = checkkey(xx)
       if key:
          if not oip == myip:
                  oldkey = f"{key};{oip};{date}"
                  newkey = f"{key};{myip};{date}"
                  with open('keys.txt','r') as file:
                     filedata = file.read()
                     filedata = filedata.replace(oldkey,newkey)
                  with open('keys.txt','w') as file:
                      file.write(filedata)
                  tedd = f'''<p style="color:green">Your ip changed {oip} to {myip} And Auto updated to System</p>'''

    key,ip,date = checkkey(myip)
    msg = "Your Key"
    if not key:
        return f'''
        <center>
<h1>Click Here to Get Your Key<p><button style="font-size: 50px;width: 100%;text-align: center;background-color: #04AA6D;"><a href="{keyurl}">Get key</a></button></h1>
</center>
'''
    date = parser.parse(date)
    datenow = datetime.now()
    diff = datenow - date
    hours,minutes,seconds = getexpire(diff.days, diff.seconds)
    resp = make_response (f'''
      <center>
      <h1>{msg}</h1>
      <p style="font-size:50px;padding: 0 7em 2em 0;border-width: 5px; border-color: green; border-style:solid;"></br>{key}</br></br>KeyIp: {ip}</br></br>{tedd}<h2>Valied Untill : {hours}H:{minutes}M:{seconds}S</h2></p>
      </center>
''')
    resp.set_cookie('ip', key, max_age=90 * 60 * 60 * 24)
    return resp

@app.route("/chat", methods=["POST"])
def chat():
    # Create a SOCKS connection
    socks_conn = socks.socksocket()

    # Wrap the SOCKS connection in an SSL/TLS context
    ssl_conn = ssl.wrap_socket(socks_conn, ssl_version=ssl.PROTOCOL_TLSv1)

    # Send and receive chat messages using the SSL/TLS-wrapped SOCKS connection
    message = request.form["message"]
    ssl_conn.send(message.encode())
    response = ssl_conn.recv(1024).decode()
    return response


@app.route('/nwkey')
def hhgt():
    ip = getip()
    key,ip,date = checkkey(ip)
    if not key:
       createkey()
    return redirect('/')


@app.route('/login/<key>')
def check(key):
    if os.path.exists('admin.txt'):
      with open('admin.txt') as f:
         lines2 = f.read().splitlines()
      if key in lines2:
         return "true"
    myip = getip()
    key,ip,date = checkkey(key,ip=False)
    if key and (myip == ip):
       return "true"
    return "false"


@app.route('/mykey')
def hg1h():
    myip = getip()
    key,ip,date = checkkey(myip)
    if key:
       return key
    else:
        return ""




@app.route('/total')
def hefllox_wxord():
    x1 = 0
    if os.path.exists('keys.txt'):
         with open('keys.txt') as f:
              lines = f.read().splitlines()
         for i in lines:
            if i == "":
              continue
            x1 = x1 + 1
    return f"<h2>Total keys {x1}<br/>"








# Load the JSON database file into memory
with open("users.json") as f:
    users = json.load(f)

@app.route("/register", methods=["POST"])
def register():
    # Accept user input for the email, username, and password
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]

    # Add the new user to the JSON database
    users[email] = {
        "username": username,
        "password": password,
    }

    # Save the updated JSON database to the file
    with open("users.json", "w") as f:
        json.dump(users, f)

    return "ลงทะเบียนผู้ใช้สำเร็จ"

@app.route("/login", methods=["POST"])
def login():
    session.permanent = True
app.permanent_session_lifetime = timedelta(minutes=30)
redirect(url_for('http://13.58.115.54:8000/login'))
    # Accept user input for the email and password
    email = request.form["email"]
    password = request.form["password"]

    # Verify the email and password against the stored credentials
    if email in users and users[email]["password"] == password:
        # Create a SOCKS connection
        socks_conn = socks.socksocket()

        # Wrap the SOCKS connection in an SSL/TLS context
        ssl_conn = ssl.wrap_socket(socks_conn, ssl_version=ssl.PROTOCOL_TLSv1)

        # Send and receive chat messages using the SSL/TLS-wrapped SOCKS connection
        message = request.form["message"]
        ssl_conn.send(message.encode())
        response = ssl_conn.recv(1024).decode()
        return response
    else:
        return "อีเมลหรือรหัสผ่านไม่ถูกต้อง"

if __name__ == "__main__":
    app.run()
