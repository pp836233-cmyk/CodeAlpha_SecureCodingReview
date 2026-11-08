"""
Secured version of app.py - all 8 findings remediated.
CodeAlpha Cyber Security Internship - Task 3

Run:  export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
      python app_fixed.py
"""
import os, re, json, sqlite3, subprocess
from flask import Flask, request, abort, render_template_string, send_from_directory
from markupsafe import escape
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]                 # (1) from environment, not source code
UPLOAD_DIR = os.path.abspath("uploads")
DB = "users.db"

@app.route("/login", methods=["POST"])
def login():
    u = request.form.get("username", "")
    p = request.form.get("password", "")
    row = sqlite3.connect(DB).execute(
        "SELECT pw FROM users WHERE name = ?", (u,)).fetchone()   # (3) parameterized query
    # (2) passwords stored with generate_password_hash (salted scrypt/PBKDF2)
    if row and check_password_hash(row[0], p):
        return "Welcome " + str(escape(u))
    return "Invalid credentials", 401

@app.route("/search")
def search():
    term = request.args.get("q", "")
    return render_template_string("<h1>Results for {{ t }}</h1>", t=term)   # (4) auto-escaped

@app.route("/download")
def download():
    return send_from_directory(UPLOAD_DIR, request.args.get("file", ""))    # (5) blocks ../

@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    if not re.fullmatch(r"[A-Za-z0-9.\-]{1,253}", host):      # (6) allow-list validation
        abort(400)
    out = subprocess.run(["ping", "-c", "1", host], capture_output=True,
                         text=True, timeout=5)                # no shell, argument list
    return out.stdout

@app.route("/load", methods=["POST"])
def load():
    try:
        return json.dumps(json.loads(request.data))           # (7) JSON instead of pickle
    except ValueError:
        abort(400)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False)                    # (8) localhost, debug off
