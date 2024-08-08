from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import db, User, Product, Order, OrderItem
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)
bcrypt = Bcrypt()

def init_routes(app):
    app.register_blueprint(main)

@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.products'))
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.products'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.products'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.products'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        birth_date = request.form.get('birth_date')
        cpf = request.form.get('cpf')
        address = request.form.get('address')
        phone = request.form.get('phone')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            email=email,
            password=hashed_password,
            full_name=full_name,
            birth_date=birth_date,
            cpf=cpf,
            address=address,
            phone=phone
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('main.products'))
    return render_template('register.html')

@main.route('/products')
@login_required
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)
    



    '''@app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.get_or_none(User.email == email, User.is_admin == True)
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['is_admin'] = True
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid credentials', 'danger')
        return render_template('admin/login.html')'''

    '''@app.route('/admin/dashboard')
    def admin_dashboard():
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        products = Product.select()
        orders = Order.select()
        return render_template('admin/dashboard.html', products=products, orders=orders)
    
    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out.', 'success')
        return redirect(url_for('home'))
    
    @app.route('/admin/products/add', methods=['GET', 'POST'])
    def admin_add_product():
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            image_url = request.form['image_url']
            Product.create(name=name, description=description, price=price, image_url=image_url)
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/add_product.html')
    
    @app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
    def admin_edit_product(product_id):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        product = Product.get_by_id(product_id)
        if request.method == 'POST':
            product.name = request.form['name']
            product.description = request.form['description']
            product.price = request.form['price']
            product.image_url = request.form['image_url']
            product.save()
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/edit_product.html', product=product)
    @app.route('/admin/products/delete/<int:product_id>')
    def admin_delete_product(product_id):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        product = Product.get_by_id(product_id)
        product.delete_instance()
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/products', methods=['GET', 'POST'])
    def admin_products():
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            image_url = request.form['image_url']
            Product.create(name=name, description=description, price=price, image_url=image_url)
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/products.html')

    @app.route('/admin/orders')
    def admin_orders():
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        orders = Order.select()
        return render_template('admin/orders.html', orders=orders)

    @app.route('/admin/orders/update/<int:order_id>', methods=['POST'])
    def update_order_status(order_id):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        order = Order.get_by_id(order_id)
        order.status = request.form['status']
        order.updated_at = datetime.now()
        order.save()
        return redirect(url_for('admin_orders'))'''
    
    '''@app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            full_name = request.form['full_name']
            birth_date = request.form['birth_date']
            cpf = request.form['cpf']
            address = request.form['address']
            phone = request.form['phone']

            existing_user = User.get_by_email(email)
            if existing_user is None:
                new_user = User(
                    email=email,
                    full_name=full_name,
                    birth_date=birth_date,
                    cpf=cpf,
                    address=address,
                    phone=phone
                )
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                session['user_id'] = new_user.id
                session['email'] = new_user.email
                session['full_name'] = new_user.full_name
                session['is_admin'] = new_user.is_admin
                flash('You have been registered successfully!', 'success')
                return redirect(url_for('products'))
            else:
                flash('Email already registered', 'danger')

        return render_template('register.html')'''
    
    '''@app.route('/register_admin', methods=['GET', 'POST'])
    def register_admin():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            hashed_password = generate_password_hash(password)
            try:
                User.create(email=email, password=hashed_password, is_admin=True)
                flash('Admin registration successful. Please log in.', 'success')
                return redirect(url_for('login'))
            except IntegrityError:
                flash('Email already registered', 'danger')
        return render_template('admin/register_admin.html')'''


    '''@app.route('/login', methods=['GET', 'POST'])
    def login():
        if 'user_id' in session:
            return redirect(url_for('products'))

        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.get_by_email(email)
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['email'] = user.email
                session['full_name'] = user.full_name
                session['is_admin'] = user.is_admin
                flash('You have been logged in!', 'success')
                return redirect(url_for('products'))
            else:
                flash('Invalid credentials', 'danger')
        return render_template('login.html')'''

    # Client Routes
    '''@app.route('/products')
    def products():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        # Recupera os produtos do banco de dados e os exibe na página
        products = Product.query.all()
        return render_template('products.html', products=products)'''


    '''@app.route('/product/<int:product_id>')
    def product_detail(product_id):
        product = Product.get_by_id(product_id)
        return render_template('product_detail.html', product=product)

    @app.route('/cart')
    def cart():
        # Implementar exibição carrinho de compras do usuário
        pass

    @app.route('/checkout', methods=['POST'])
    def checkout():
        # Implementar finalização do pedido
        pass'''
