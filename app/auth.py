from flask import render_template, redirect, session, url_for, Blueprint, flash, request
from .models import Order, OrderItem, Product, User
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
@login_required
def adm_Dashboard():
    if not current_user.admin:
        flash('Admin status is required to access this page.', category='danger') 
        return redirect(url_for('auth.products'))
    
    users = User.query.all()
    products = Product.query.all()
    return render_template('showdata.html', users=users, products=products)

@auth.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    if not current_user.admin:
        flash('Acesso negado. Apenas administradores podem alterar o status dos pedidos.', 'danger')
        return redirect(url_for('auth.admin_orders'))

    order = Order.query.get_or_404(order_id)
    
    new_status = request.form.get('status')

    if new_status:
        order.status = new_status
        db.session.commit()
        flash(f'Status do pedido #{order.id} atualizado para {new_status}', 'success')
    else:
        flash('Selecione um status válido.', 'danger')

    return redirect(url_for('auth.admin_orders'))


@auth.route('/Add_Product', methods=['GET', 'POST'])
@login_required
def addprod():
    if not current_user.admin:
        flash('Admin status is required to access this page.', category='danger') 
        return redirect(url_for('auth.products'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        image = request.form.get('image')
        
        productname = Product.query.filter_by(name=name).first()

        if productname:
          flash('Product already registered.', category='danger')                      
        else:
            new_product = Product(name=name, price=price, image=image, description=description)
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully', category='success')
            return redirect(url_for('auth.addprod'))
    
    return render_template('prod_add.html')

@auth.route('/Edit_Product/<int:id>', methods=['GET', 'POST'])
@login_required
def editprod(id): 
     if not current_user.admin:
        flash('Admin status is required to access this page.', category='danger') 
        return redirect(url_for('auth.products'))
     
     product = Product.query.get(id)

     if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = request.form.get('price')
        product.description = request.form.get('description')

        db.session.commit()
        flash('Product updated successfully', category='success')
        return redirect(url_for('auth.editprod', id=product.id))

     return render_template('prod_edit.html', product=product)

@auth.route('/Delete_Product/<int:id>', methods=['POST'])
@login_required
def delprod(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', category='success')
    return redirect(url_for('auth.products'))

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
        elif len(cpf) != 11: #This CPF validation will be changed to a real CPF validation.
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


@auth.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash('Product not found.', category='danger')
        return redirect(url_for('auth.products'))

    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'name': product.name, 'price': product.price, 'quantity': 1, 'image': product.image}
    
    session['cart'] = cart
    flash('Product added to cart!', category='success')
    return redirect(url_for('auth.products'))


@auth.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

@auth.route('/cart/increase/<int:product_id>')
@login_required
def increase_quantity(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
        session['cart'] = cart
    return redirect(url_for('auth.cart'))

@auth.route('/cart/decrease/<int:product_id>')
@login_required
def decrease_quantity(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart and cart[str(product_id)]['quantity'] > 1:
        cart[str(product_id)]['quantity'] -= 1
        session['cart'] = cart
    else:
        flash('Minimum quantity is 1.', category='danger')
    
    return redirect(url_for('auth.cart'))


@auth.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    
    if str(product_id) in cart:
        cart.pop(str(product_id))
        session['cart'] = cart
        flash('Item removido do carrinho.', category='success')
    else:
        flash('Item não encontrado no carrinho.', category='danger')
    
    return redirect(url_for('auth.cart'))

@auth.route('/clear_cart', methods=['POST'])
@login_required
def clear_cart():
    session.pop('cart', None)
    flash('Carrinho esvaziado.', category='success')
    return redirect(url_for('auth.cart'))


@auth.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty.', category='danger')
        return redirect(url_for('auth.products'))
    
    new_order = Order(user_id=current_user.id, status='Pendente', total=sum(item['price'] * item['quantity'] for item in cart.values()))
    db.session.add(new_order)
    db.session.commit()

    for product_id, item in cart.items():
        order_item = OrderItem(order_id=new_order.id, product_id=int(product_id), quantity=item['quantity'])
        db.session.add(order_item)
    
    db.session.commit()
    session.pop('cart', None)
    flash('Order placed successfully!', category='success')
    return redirect(url_for('auth.my_orders'))

@auth.route('/my_orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('my_orders.html', orders=orders)

@auth.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    order = Order.query.get(order_id)


    if order and order.user_id == current_user.id:
        if order.status == "Pendente":
            order.status = "Cancelado"
            db.session.commit()
            flash('Pedido cancelado com sucesso!', 'success')
        else:
            flash('Somente pedidos pendentes podem ser cancelados.', 'warning')
    else:
        flash('Pedido não encontrado ou não autorizado.', 'danger')

    return redirect(url_for('auth.my_orders'))


@auth.route('/admin_orders')
@login_required
def admin_orders():
    if not current_user.admin:
        flash('Admin access required.', category='danger')
        return redirect(url_for('auth.products'))
    
    orders = Order.query.all()
    return render_template('admin_orders.html', orders=orders)
