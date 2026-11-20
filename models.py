from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import string

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    description = db.Column(db.Text, nullable=False)
    poster = db.Column(db.String(500), default='default_poster.jpg')
    trailer = db.Column(db.String(500), default='')
    release_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='now_showing')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shows = db.relationship('Show', backref='movie', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='movie', lazy=True)
    
    def __repr__(self):
        return f'<Movie {self.title}>'

class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    theatre = db.Column(db.String(200), nullable=False)
    show_date = db.Column(db.Date, nullable=False)
    show_time = db.Column(db.Time, nullable=False)
    screen = db.Column(db.String(50), default='Screen 1')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    seats = db.relationship('Seat', backref='show', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='show', lazy=True)
    
    @property
    def datetime(self):
        from datetime import datetime
        return datetime.combine(self.show_date, self.show_time)
    
    def __repr__(self):
        return f'<Show {self.theatre} {self.show_date} {self.show_time}>'

class Seat(db.Model):
    __tablename__ = 'seats'
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='available')
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=True)
    
    def __repr__(self):
        return f'<Seat {self.seat_number} {self.status}>'

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    seats = db.Column(db.String(500), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='confirmed')
    seat_objects = db.relationship('Seat', backref='booking', lazy=True)
    
    @staticmethod
    def generate_booking_id():
        prefix = 'BMS'
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"{prefix}{suffix}"
    
    def __repr__(self):
        return f'<Booking {self.booking_id}>'