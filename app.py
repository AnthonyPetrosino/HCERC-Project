import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Connects to db
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()  # Connect to db
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()  # Execute sql query 
    
    conn.close()    # Close connection to db
    if post is None:    # If post doesn't exist, 404 error
        abort(404)
    return post

# Homepage route
# @app.route("/")
# def index():
#     return render_template("index.html")

# Homepage route
@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()  # Fetch all rows
    conn.close()
    return render_template("index.html", posts=posts)

# Individual post
@app.route('/<int:post_id>')    # Variable rule 
def post(post_id):
    post = get_post(post_id)    # Uses previous function
    return render_template('post.html', post=post)

# Form allowing user to create a post
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':    # Executes following POST request
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required.')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))   
            conn.commit()
            conn.close()
            flash('Post created')
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required.')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)       
     
# Dockerize app
if __name__ == "__main__":
    # Run app on port 5000 outside of the container
    app.run(host='0.0.0.0', port=5000, debug=True)