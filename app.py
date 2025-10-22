from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def get_posts():
    """Eine Hilfsfunktion, um Posts aus der JSON-Datei zu laden."""
    with open('blog_posts.json', 'r') as f:
        return json.load(f)

def save_posts(posts):
    """Eine Hilfsfunktion, um Posts in die JSON-Datei zu speichern."""
    with open('blog_posts.json', 'w') as f:
        json.dump(posts, f, indent=4)


@app.route('/')
def index():
    blog_posts = get_posts()
    return render_template('index.html', posts=blog_posts)


# Neue Route zum Hinzufügen von Beiträgen
@app.route('/add', methods=['GET', 'POST'])
def add():
    # Wenn das Formular abgeschickt wurde (POST-Request)
    if request.method == 'POST':
        # 1. Daten aus dem Formular holen
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # 2. Bestehende Beiträge laden
        posts = get_posts()

        # 3. Eine neue, eindeutige ID generieren
        # Wir nehmen die ID des letzten Posts und addieren 1.
        # Wenn es keine Posts gibt, starten wir mit 1.
        if posts:
            new_id = posts[-1]['id'] + 1
        else:
            new_id = 1

        # 4. Neuen Beitrag als Dictionary erstellen
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        # 5. Neuen Beitrag zur Liste hinzufügen und speichern
        posts.append(new_post)
        save_posts(posts)

        # 6. Zurück zur Startseite umleiten
        return redirect(url_for('index'))

    # Wenn die Seite normal aufgerufen wird (GET-Request), zeige das Formular
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)