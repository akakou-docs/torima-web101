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

@app.route("/_torima/back", methods=['GET'])
def back():
    return redirect('/')


@app.route("/", methods=['GET'])
def show_posts():
    user_id = authenticate()
    return render_template('index.html', posts=posts, user_id=user_id)

@app.route("/new", methods=['POST'])
def create_post():
    user_id = authenticate()

    content = request.form["content"]
    posts.append({
        'content': content,
        'user_id': user_id
    })

    return render_template('index.html', posts=posts, user_id=user_id)


@app.route("/delete", methods=['POST'])
def delete_post():
    user_id = authenticate()
    content_id = int(request.form["content"])

    port = posts[content_id]

    if port['user_id'] == user_id:
        del posts[content_id]
        return render_template('index.html', posts=posts, user_id=user_id)
    else:
        return "authentication failed"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000)