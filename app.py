from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def get_posts():
    """Eine Hilfsfunktion, um Posts aus der JSON-Datei zu laden."""
    try:
        with open('blog_posts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_posts(posts):
    """Eine Hilfsfunktion, um Posts in die JSON-Datei zu speichern."""
    with open('blog_posts.json', 'w') as f:
        json.dump(posts, f, indent=4)


@app.route('/')
def index():
    blog_posts = get_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        posts = get_posts()
        if posts:
            new_id = posts[-1]['id'] + 1
        else:
            new_id = 1
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('add.html')


# NEUE ROUTE ZUM LÖSCHEN VON BEITRÄGEN
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    # 1. Alle aktuellen Beiträge laden
    posts = get_posts()

    # 2. Eine neue Liste erstellen, die alle Beiträge außer dem zu löschenden enthält
    posts_after_deletion = [post for post in posts if post['id'] != post_id]

    # 3. Die neue, gefilterte Liste in die JSON-Datei zurückspeichern
    save_posts(posts_after_deletion)

    # 4. Zurück zur Startseite umleiten
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)