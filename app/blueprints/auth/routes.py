from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    return render_template('auth/index.html')

@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    elif request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        password = request.form.get('password')
        birth_date = request.form.get('birth_date')
        address = request.form.get('address')
        phone = request.form.get('phone')

        cpfcheck = User.query.filter_by(cpf=cpf).first()
        emailcheck = User.query.filter_by(email=email).first()
        
        if cpfcheck:
            flash('Este CPF já está registrado.', category='danger')
        elif emailcheck:
            flash('Este E-mail já está registrado.', category='danger')
        elif len(first_name) < 2:
            flash('O nome deve conter mais de um caractere.', category='danger')
        elif len(last_name) < 2:
            flash('O último nome deve conter mais de um caractere', category='danger')
        elif len(cpf) != 11: #Validação de CPF será substituída por uma validação de CPF real.
            flash('Insira um CPF válido', category='danger')
        elif len(email) < 4: #Validação de E-mail será substituída por uma validação de E-mail real.
            flash('E-mail deve conter mais de 3 caracteres', category='danger')
        elif len(password) < 6:
            flash('Sua senha deve conter pelo menos 6 caracteres', category='danger')
        
        else:
            new_user = User(first_name=first_name, last_name=last_name, cpf=cpf, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'), birth_date=birth_date, address=address, phone=phone)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Conta criada com sucesso', category='success')
            return redirect(url_for('auth.home'))
        
    return render_template('auth/sign_in.html')


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
                return redirect(url_for('auth.home'))
            else:
                flash('E-mail ou senha incorretos. Tente novamente.', category='danger')
        else:
            flash('E-mail não registrado', category='danger')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/my_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    user = current_user
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        if email and email != user.email:
            emailcheck = User.query.filter_by(email=email).first()
            if emailcheck:
                flash('Este E-mail já está registrado.', category='danger')
                return render_template('auth/my_profile.html')
            
            user.email = email
        


        if password and len(password) >= 6:
            user.password = generate_password_hash(password, method='pbkdf2:sha256')

        if password and len(password) < 6:
            flash('A senha deve conter pelo menos 6 caracteres.', category='danger')
            return render_template('auth/my_profile.html')            
        
        if address and address != user.address:
            user.address = address

        if phone and phone != user.phone:
            user.phone = phone

        db.session.commit()
        flash('Dados atualizados com sucesso!', 'success')
        return redirect(url_for('auth.update_profile'))

    return render_template('auth/my_profile.html')
