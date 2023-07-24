from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    cart = db.relationship("Product", secondary="cart")

    def __init__(self, username, password, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def add_to_cart(self, product):
        p = Cart(self.id, product)
        db.session.add(p)
        db.session.commit()

    def remove_from_cart(self, product):
        p = Cart.query.filter_by(user_id=self.id).filter_by(product_id=product.id).first()
        db.session.delete(p)
        db.session.commit()

    def get_cart(self):
        p = Cart.query.filter_by(user_id=self.id).all()
        cart = [Product.query.get(obj.product_id) for obj in p]
        return cart
    


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name =  db.Column(db.String(5000),nullable=False)
    description =  db.Column(db.String(5000),nullable=False)
    category = db.Column(db.String(5000),nullable=False)
    image = db.Column(db.String(5000),nullable=False)
    rating = db.Column(db.Float,nullable=False)
    price = db.Column(db.Float,nullable=False)

    def __init__(self, id, name, description, category, image, rating, price):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.image = image
        self.rating = rating
        self.price = price


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id












