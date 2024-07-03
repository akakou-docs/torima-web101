import hashlib
import secrets
from flask import Flask, redirect, request, render_template
import os
app = Flask(__name__)

posts = []

APP_TOKEN = secrets.token_urlsafe(32).encode('ascii')

def authenticate():
    user_id = request.headers.get('X-Torima-UserID', '').encode('ascii')
    if not user_id:
        return None

    hashed_id = hashlib.sha224(user_id + APP_TOKEN).hexdigest()

    return hashed_id


@app.route("/", methods=['GET'])
def show_posts():
    return render_template('index.html', posts=posts)

@app.route("/post", methods=['POST'])
def create_post():
    user_id = authenticate()

    content = request.form["content"]
    posts.append({
        'content': content,
        'user_id': user_id
    })

    return render_template('index.html', posts=posts)


@app.route("/_torima/back", methods=['GET'])
def back():
    return redirect('/')

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000)