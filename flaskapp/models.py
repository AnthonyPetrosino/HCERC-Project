from flaskapp import db, LoginManager
from datetime import datetime
from flask_login import UserMixin

# To update db:
# flask db migrate -m "Initial Migration"     (changes can be seen in the migrations -> versions directory)
# flask db upgrade

# Login returning user functionality
@LoginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User models 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)    # Allows us to get all of the posts this user created

    averageSuccess = db.Column(db.Integer, nullable=True)

    def __repr__(self):  # How to 'print' objects
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   # Specifies which user this post belongs to

    price_at_creation = db.Column(db.Double, nullable=False)
    ticker = db.Column(db.String(10), nullable=False)
    sector = db.Column(db.Integer, nullable=False) 
    action = db.Column(db.String(10), nullable=False) 
    
    pdf_file = db.Column(db.String(255), nullable=True)

    def __repr__(self):  # How to 'print' objects
        return f"Post('{self.title}', '{self.date_posted}', '{self.ticker}')"
