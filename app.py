"""
INTENTIONALLY VULNERABLE Flask app - for educational code review only.
DO NOT deploy or run this on a public network.
CodeAlpha Cyber Security Internship - Task 3
"""
import sqlite3, hashlib, os, pickle, subprocess
from flask import Flask, request, render_template_string, send_file

app = Flask(__name__)
app.secret_key = "admin123"                      # (1) hard-coded secret
DB = "users.db"

@app.route("/login", methods=["POST"])
def login():
    u = request.form["username"]
    p = hashlib.md5(request.form["password"].encode()).hexdigest()   # (2) weak hash
    q = "SELECT * FROM users WHERE name='%s' AND pw='%s'" % (u, p)   # (3) SQL injection
    row = sqlite3.connect(DB).execute(q).fetchone()
    return "Welcome " + u if row else "Invalid"

@app.route("/search")
def search():
    term = request.args.get("q", "")
    return render_template_string("<h1>Results for " + term + "</h1>")  # (4) XSS / SSTI

@app.route("/download")
def download():
    return send_file("uploads/" + request.args["file"])           # (5) path traversal

@app.route("/ping")
def ping():
    host = request.args["host"]
    return subprocess.getoutput("ping -c 1 " + host)              # (6) command injection

@app.route("/load", methods=["POST"])
def load():
    return str(pickle.loads(request.data))                        # (7) insecure deserialization

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)                           # (8) debug mode exposed
