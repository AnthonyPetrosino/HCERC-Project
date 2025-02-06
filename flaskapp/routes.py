from flaskapp import app, db
from flaskapp.models import User, Post
from flaskapp.forms import RegistrationForm, LoginForm
import yfinance as yf
from flask import render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import abort

# Homepage route
@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

# Viewing an individual post
@app.route('/<int:post_id>')    
def post(post_id):
    post = Post.query.get_or_404(post_id)  

    price_at_creation = float(post.price_at_creation)
    ticker = post.ticker.strip().upper()

    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period="5d")
        if stock_data.empty:
            raise ValueError("Stock data unavailable")

        cur_price = stock_data['Close'].iloc[-1]
        cur_price = f"{cur_price:.2f}"
        percent_change = ((float(cur_price) - price_at_creation) / price_at_creation) * 100
        percent_change = f"{percent_change:.2f}"
    except Exception:
        cur_price = "Price not available"
        percent_change = "N/A"

    return render_template(
        'post.html',
        post=post,
        cur_price=cur_price,
        price_at_creation=price_at_creation,
        percent_change=percent_change,
    )


# Handle requests allowing user to create a post
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':    # Executes following POST request
        title = request.form['title']
        content = request.form['content']
        ticker = request.form['ticker'].upper()
        # user = request.form['user'] TODO

        if not title or not ticker or not content:
            flash('Please fill out all parts of the form.', 'danger')
            return render_template('create.html')
        
        # Query current stock data to store as original price
        try:
            stock = yf.Ticker(ticker)           # Pass it to yfinance
            stock_data = stock.history(period="5d")     # Fetch most recent day's data
            cur_price = stock_data['Close'].iloc[-1] if not stock_data.empty else None  # Fetch previous day's data if after hours
            cur_price = f"{cur_price:.2f}" if cur_price else "N/A"
        except Exception as e:
            cur_price = "Error fetching price" # TODO Error

        if cur_price == "N/A":
            flash('Please check that your ticker symbol.', 'danger')
            return render_template('create.html')
        
        # Create and save post
        new_post = Post(
            title=title,
            content=content,
            ticker=ticker,
            price_at_creation=cur_price,
            user_id=1  # TODO: Change this to the actual logged-in user's ID
        )
        
        db.session.add(new_post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('index'))
    return render_template('create.html')

# # Handle requests allowing user to edit a post
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title:
            flash('Title is required.', 'danger')
        else:
            post.title = title
            post.content = content
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('index'))
        
    return render_template('edit.html', post=post)       

# # Handle requests allowing user to delete a post
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash(f'"{post.title}" was successfully deleted!', 'danger')
    return redirect(url_for('index'))

# # User authentication
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