from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    # Öffne die JSON-Datei im Lesemodus ('r')
    with open('blog_posts.json', 'r') as f:
        # Lade den Inhalt der Datei in die Variable 'blog_posts'
        blog_posts = json.load(f)

    # Gib die Variable 'blog_posts' unter dem Namen 'posts' an das Template weiter
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)