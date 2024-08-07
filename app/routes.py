from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Product, Order, OrderItem
from peewee import IntegrityError
from datetime import datetime

def init_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/admin/login', methods=['GET', 'POST'])
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
        return render_template('admin/login.html')

    @app.route('/admin/dashboard')
    def admin_dashboard():
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        products = Product.select()
        orders = Order.select()
        return render_template('admin/dashboard.html', products=products, orders=orders)
    
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
        return redirect(url_for('admin_orders'))
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            hashed_password = generate_password_hash(password)
            try:
                User.create(email=email, password=hashed_password, is_admin=False)
                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('login'))
            except IntegrityError:
                flash('Email already registered', 'danger')
        return render_template('register.html')
    


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.get_or_none(User.email == email)
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['is_admin'] = user.is_admin
                return redirect(url_for('admin_dashboard') if user.is_admin else url_for('products'))
            else:
                flash('Invalid email or password', 'danger')
        return render_template('index.html')

    # Client Routes
    @app.route('/products')
    def products():
        products = Product.select()
        return render_template('products.html', products=products)

    @app.route('/product/<int:product_id>')
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
        pass
