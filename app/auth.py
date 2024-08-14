from flask import render_template, redirect, url_for, Blueprint, flash, request
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    return render_template('index.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login Succesful!', category='success')
                return redirect(url_for('auth.home'))
            else:
                flash('Incorrect User or Password. Check and try again.', category='danger')

    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    return render_template('logout.html')

@auth.route('/products')
def products():
    return render_template('products.html')

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        password = request.form.get('password')
        birth_date = request.form.get('birth_date')
        adress = request.form.get('adress')
        phone = request.form.get('phone')

        cpfcheck = User.query.filter_by(cpf=cpf).first()
        emailcheck = User.query.filter_by(email=email).first()
        
        if cpfcheck:
            flash('CPF is already registered.', category='danger')
        elif emailcheck:
            flash('E-mail is already registered.', category='danger')
        elif len(first_name) < 2:
            flash('Name must be more than a single character', category='danger')
        elif len(last_name) < 2:
            flash('Last name must be more than a single character', category='danger')
        elif len(cpf) != 11:
            flash('Enter a valid CPF number', category='danger')
        elif len(email) < 4:
            flash('E-mail must be greater than 3 characters', category='danger')
        elif len(password) < 6:
            flash('Password must have at least 6 characters', category='danger')
        
        else:
            new_user = User(first_name=first_name, last_name=last_name, cpf=cpf, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'), birth_date=birth_date, adress=adress, phone=phone)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created Succesfully', category='success')
            return redirect(url_for('auth.home'))
        
    return render_template('sign_in.html')