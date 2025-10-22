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
            "content": content,
            "likes": 0  # Stelle sicher, dass neue Posts mit 0 Likes starten
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


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        updated_author = request.form.get('author')
        updated_title = request.form.get('title')
        updated_content = request.form.get('content')
        all_posts = get_posts()
        for p in all_posts:
            if p['id'] == post_id:
                p['author'] = updated_author
                p['title'] = updated_title
                p['content'] = updated_content
                break
        save_posts(all_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


# NEUE ROUTE FÜR DAS LIKEN VON BEITRÄGEN
@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    # 1. Alle Beiträge laden
    posts = get_posts()

    # 2. Den richtigen Beitrag finden und die Likes erhöhen
    for post in posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1
            break

    # 3. Die aktualisierte Liste speichern
    save_posts(posts)

    # 4. Zurück zur Startseite umleiten
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)