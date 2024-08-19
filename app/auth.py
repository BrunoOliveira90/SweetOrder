from flask import render_template, redirect, url_for, Blueprint, flash, request
from .models import Product, User
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
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect User or Password. Check and try again.', category='danger')
        else:
            flash('E-mail not registered', category='danger')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@auth.route('/Admin_Dashboard')
def adm_Dashboard():
    users = User.query.all()
    return render_template('showdata.html', users=users)

@auth.route('/Add_Product', methods=['GET', 'POST'])
@login_required
def addprod():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        
        productname = Product.query.filter_by(name=name).first()

        if productname:
          flash('Product already registered.', category='danger')                      
        else:
            new_product = Product(name=name, price=price, description=description)
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully', category='success')
            return redirect(url_for('auth.addprod'))
    
    return render_template('prod_add.html')

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    elif request.method == 'POST':
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
            login_user(new_user, remember=True)
            flash('Account created Succesfully', category='success')
            return redirect(url_for('views.home'))
        
    return render_template('sign_in.html')