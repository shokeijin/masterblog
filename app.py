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


def fetch_post_by_id(post_id):
    """Findet einen einzelnen Beitrag anhand seiner ID."""
    posts = get_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


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


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    posts = get_posts()
    posts_after_deletion = [post for post in posts if post['id'] != post_id]
    save_posts(posts_after_deletion)
    return redirect(url_for('index'))


# NEUE ROUTE ZUM BEARBEITEN VON BEITRÄGEN
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Finde den zu bearbeitenden Beitrag
    post = fetch_post_by_id(post_id)
    if post is None:
        # Wenn der Beitrag nicht existiert, gib einen Fehler zurück
        return "Post not found", 404

    # Wenn das Formular abgeschickt wurde (POST)
    if request.method == 'POST':
        # Hole die aktualisierten Daten aus dem Formular
        updated_author = request.form.get('author')
        updated_title = request.form.get('title')
        updated_content = request.form.get('content')

        # Lade alle Beiträge, finde den richtigen und aktualisiere ihn
        all_posts = get_posts()
        for p in all_posts:
            if p['id'] == post_id:
                p['author'] = updated_author
                p['title'] = updated_title
                p['content'] = updated_content
                break

        # Speichere die aktualisierte Liste und leite zur Startseite um
        save_posts(all_posts)
        return redirect(url_for('index'))

    # Wenn die Seite normal aufgerufen wird (GET), zeige das Formular an
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)