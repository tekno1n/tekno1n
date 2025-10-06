from flask import Flask, request, Response, send_from_directory, jsonify
from functools import wraps
import time, os
from collections import defaultdict

APP_TITLE = "Tekno1n.id | Premium Digital Store"
ADMIN_USER = "tekno1n"
ADMIN_PASS = "superkuat123"

app = Flask(__name__, static_folder='public')

# Rate limit: 60 req/60s per IP
WINDOW = 60
MAX_REQ = 60
buckets = defaultdict(list)

def rate_limiter():
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "unknown"
    now = time.time()
    q = buckets[ip]
    while q and q[0] < now - WINDOW:
        q.pop(0)
    if len(q) >= MAX_REQ:
        return False
    q.append(now)
    return True

@app.before_request
def _rl():
    if not rate_limiter():
        return jsonify({"error":"Too Many Requests"}), 429

def check(u, p): return u == ADMIN_USER and p == ADMIN_PASS
def need_auth():
    return Response('Auth required', 401, {'WWW-Authenticate':'Basic realm="tekno1n admin"'})
def requires_auth(f):
    @wraps(f)
    def w(*args, **kwargs):
        auth = request.authorization
        if not auth or not check(auth.username, auth.password):
            return need_auth()
        return f(*args, **kwargs)
    return w

@app.route('/')
def home():
    # inject WA number placeholder replacement already in file, so just serve
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/admin')
@requires_auth
def admin():
    return f"<h2>{APP_TITLE}</h2><p>Halo admin tekno1n 👋</p><ul><li>Traffic OK</li><li>Rate limit aktif</li></ul>"

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # listen local only, aman untuk di-tunnel
    app.run(host='127.0.0.1', port=8080)
