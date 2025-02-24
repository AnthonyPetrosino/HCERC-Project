from flaskapp import app, db, bcrypt
from flaskapp.models import User, Post
from flaskapp.forms import RegistrationForm, LoginForm
import yfinance as yf
from flask import render_template, request, url_for, flash, redirect, jsonify, request
from werkzeug.exceptions import abort
from flask_login import login_user, current_user, logout_user, login_required

# Homepage route
@app.route("/")
def index():
    posts = Post.query.all()

    for post in posts:
        price_at_creation = float(post.price_at_creation)
        ticker = post.ticker.strip().upper()

        try:
            stock = yf.Ticker(ticker)
            stock_data = stock.history(period='5d')
            if stock_data.empty:
                raise ValueError("Stock data unavailable")

            cur_price = stock_data['Close'].iloc[-1]
            percent_change = ((float(cur_price) - price_at_creation) / price_at_creation) * 100
            post.percent_change = f"{percent_change:.2f}"  # Attach percent_change to post object
        except Exception:
            post.percent_change = "N/A"

    return render_template("index.html", posts=posts)

# Viewing an individual post
@app.route('/<int:post_id>')    
def post(post_id):
    post = Post.query.get_or_404(post_id)  

    price_at_creation = float(post.price_at_creation)
    ticker = post.ticker.strip().upper()

    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period='5d') 
        if stock_data.empty:
            print("Stock data unavailable")
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
        percent_change=percent_change,
    )


# Handle requests allowing user to create a post
@app.route('/create', methods=('GET', 'POST'))
@login_required     # TODO Only allow admin to create posts
def create():
    if request.method == 'POST':    # Executes following POST request
        title = request.form['title']
        content = request.form['content']
        ticker = request.form['ticker'].upper()
        action = request.form['action']
        sector = request.form['sector']
        # user = request.form['user'] TODO

        if not title or not ticker or not content:
            flash('Please fill out all parts of the form.', 'danger')
            return render_template('create.html')
        
        # Query current stock data to store as original price
        try:
            stock = yf.Ticker(ticker)           # Pass it to yfinance
            stock_data = stock.history(period='5d')     # Fetch most recent day's data
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
            user_id=1,  # TODO: Change this to the actual logged-in user's ID
            sector=sector,
            action=action
        )
        
        db.session.add(new_post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('index'))
    return render_template('create.html')

# # Handle requests allowing user to edit a post
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required     # TODO Only allow admin to edit posts
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

# Handle requests allowing user to delete a post
@app.route('/<int:id>/delete', methods=('POST',))
@login_required     # TODO Only allow admin to delete posts
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash(f'"{post.title}" was successfully deleted!', 'danger')
    return redirect(url_for('index'))


# User authentication
# @app.route("/register", methods=('GET', 'POST'))
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Hashing password
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Account created for "{}"! Please log in.'.format(form.username.data), 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)

@app.route("/login", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Loggin unsuccessful, please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html')