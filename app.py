import sqlite3
import yfinance as yf
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import abort
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key76543267' # TODO Change

bcrypt = Bcrypt(app)

# Connects to db
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()  # Connect to db
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()  # Execute sql query 
    
    conn.close()        # Close connection to db
    if post is None:    # If post doesn't exist, 404 error
        abort(404)
    return post

# Homepage route
@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()  # Fetch all rows
    conn.close()
    return render_template("index.html", posts=posts)

# Viewing an individual post
@app.route('/<int:post_id>')    # Variable rule 
def post(post_id):
    post = get_post(post_id)

    price_at_creation = post['price_at_creation']
    ticker = post['ticker'].strip().upper()     # Retrieve ticker symbol from db

    # Query current stock data
    try:
        stock = yf.Ticker(ticker)           # Pass it to yfinance
        stock_data = stock.history(period="7d")     # Fetch most recent day's data
        cur_price = stock_data['Close'].iloc[-1] if not stock_data.empty else None  # Fetch previous day's data if after hours
        cur_price = f"{cur_price:.2f}"
    except Exception as e:
        cur_price = "Error fetching price"

    percent_change = ((float(cur_price) - float(price_at_creation)) / float(price_at_creation)) * 100
    percent_change = f"{percent_change:.2f}"

    return render_template('post.html', post=post, cur_price=cur_price, price_at_creation=price_at_creation, percent_change=percent_change)

# Handle requests allowing user to create a post
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':    # Executes following POST request
        title = request.form['title']
        content = request.form['content']
        ticker = request.form['ticker'].upper()

        # Query current stock data to store as original price
        try:
            stock = yf.Ticker(ticker)           # Pass it to yfinance
            stock_data = stock.history(period="7d")     # Fetch most recent day's data
            cur_price = stock_data['Close'].iloc[-1] if not stock_data.empty else None  # Fetch previous day's data if after hours
            cur_price = f"{cur_price:.2f}" if cur_price else "N/A"
        except Exception as e:
            cur_price = "Error fetching price"

        if not title or not ticker or not content:
            flash('Please fill out all parts of the form.', 'danger')
        elif cur_price == "N/A":
            flash('Please check that your ticker symbol.', 'danger')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content, ticker, price_at_creation) VALUES (?, ?, ?, ?)',
                         (title, content, ticker, cur_price))   
            conn.commit()
            conn.close()
            flash('Post created.', 'success')
            return redirect(url_for('index'))
    return render_template('create.html')

# Handle requests allowing user to edit a post
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

# Handle requests allowing user to delete a post
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']), 'danger')
    return redirect(url_for('index'))

# User authentication
@app.route("/register", methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for "{}".'.format(form.username.data), 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if True:
            # TODO
            flash('Logged in as "{}".'.format(form.email.data), 'success')
            return redirect(url_for('index'))
        else:
            flash('Loggin unsuccessful, please check email and password.', 'danger')
    return render_template('login.html', form=form)


# Dockerize and run app
if __name__ == "__main__":
    # Run app on port 5000 outside of the container
    app.run(host='0.0.0.0', port=5000, debug=True)