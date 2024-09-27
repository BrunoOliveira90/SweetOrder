from datetime import datetime
from . import db
from flask_login import UserMixin
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, Optional, Length
from flask_wtf import FlaskForm

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    cpf = db.Column(db.String(12))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    birth_date = db.Column(db.String(20))
    address = db.Column(db.String(250))
    phone = db.Column(db.String(12))
    admin = db.Column(db.Boolean, default=False)
    



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(5000), nullable=False)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pendente')
    items = db.relationship('OrderItem', backref='order', lazy=True)
    total = db.Column(db.Float, nullable=False)
    user = db.relationship('User', backref='orders')
    created_at = db.Column(db.DateTime, default=datetime.now)


class UpdateProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Endereço', validators=[DataRequired()])
    phone = StringField('Telefone', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Senha', validators=[Optional()])