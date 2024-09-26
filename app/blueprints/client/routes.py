from flask import Blueprint, flash, render_template, redirect, session, url_for
from flask_login import current_user, login_required
from app import auth, db
from app.models import Order, OrderItem, Product

client = Blueprint('client', __name__)

@client.route('/products')
def products():
    products = Product.query.all()
    return render_template('client/products.html', products=products)



@client.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    if current_user.admin:
        flash('Somente clientes podem acessar essa página.', 'danger')
        return redirect(url_for('auth.home'))

    product = Product.query.get(product_id)
    if not product:
        flash('Product not found.', category='danger')
        return redirect(url_for('client.products'))

    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'name': product.name, 'price': product.price, 'quantity': 1, 'image': product.image}
    
    session['cart'] = cart
    flash('Product added to cart!', category='success')
    return redirect(url_for('client.products'))


@client.route('/cart')
@login_required
def cart():
    if current_user.admin:
        flash('Somente clientes podem acessar essa página.', 'danger')
        return redirect(url_for('auth.home'))
    
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('client/cart.html', cart=cart, total=total)

@client.route('/cart/increase/<int:product_id>')
@login_required
def increase_quantity(product_id):
    if current_user.admin:
        flash('Somente clientes podem acessar essa página.', 'danger')
        return redirect(url_for('auth.home'))

    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
        session['cart'] = cart
    return redirect(url_for('client.cart'))

@client.route('/cart/decrease/<int:product_id>')
@login_required
def decrease_quantity(product_id):
    if current_user.admin:
        flash('Somente clientes podem acessar essa página.', 'danger')
        return redirect(url_for('auth.home'))
    
    cart = session.get('cart', {})
    if str(product_id) in cart and cart[str(product_id)]['quantity'] > 1:
        cart[str(product_id)]['quantity'] -= 1
        session['cart'] = cart
    else:
        flash('Minimum quantity is 1.', category='danger')
    
    return redirect(url_for('client.cart'))


@client.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):

    if current_user.admin:
        flash('Somente clientes podem acessar essa página.', 'danger')
        return redirect(url_for('auth.home'))

    cart = session.get('cart', {})
    
    if str(product_id) in cart:
        cart.pop(str(product_id))
        session['cart'] = cart
        flash('Item removido do carrinho.', category='success')
    else:
        flash('Item não encontrado no carrinho.', category='danger')
    
    return redirect(url_for('client.cart'))

@client.route('/clear_cart', methods=['POST'])
@login_required
def clear_cart():
    if current_user.admin:
        flash('Somente clientes podem acessar essa página.', 'danger')
        return redirect(url_for('auth.home'))

    session.pop('cart', None)
    flash('Carrinho esvaziado.', category='success')
    return redirect(url_for('client.cart'))


@client.route('/checkout', methods=['POST'])
@login_required
def checkout():
    if current_user.admin:
        flash('Somente clientes podem acessar essa página.', 'danger')
        return redirect(url_for('auth.home'))

    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty.', category='danger')
        return redirect(url_for('client.products'))
    
    new_order = Order(user_id=current_user.id, status='Pendente', total=sum(item['price'] * item['quantity'] for item in cart.values()))
    db.session.add(new_order)
    db.session.commit()

    for product_id, item in cart.items():
        order_item = OrderItem(order_id=new_order.id, product_id=int(product_id), quantity=item['quantity'])
        db.session.add(order_item)
    
    db.session.commit()
    session.pop('cart', None)
    flash('Order placed successfully!', category='success')
    return redirect(url_for('client.my_orders'))

@client.route('/my_orders')
@login_required
def my_orders():
    if current_user.admin:
        flash('Somente clientes podem acessar essa página.', 'danger')
        return redirect(url_for('auth.home'))
    
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('client/my_orders.html', orders=orders)

@client.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):

    if current_user.admin:
        flash('Somente clientes podem acessar essa página.', 'danger')
        return redirect(url_for('auth.home'))
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

    return redirect(url_for('client.my_orders'))

