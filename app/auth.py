from flask import render_template, redirect, session, url_for, Blueprint, flash, request
from .models import Order, OrderItem, Product, User, UpdateProfileForm
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
                return render_template('my_profile.html')
            
            user.email = email
        


        if password and len(password) >= 6:
            user.password = generate_password_hash(password, method='pbkdf2:sha256')

        if password and len(password) < 6:
            flash('A senha deve conter pelo menos 6 caracteres.', category='danger')
            return render_template('my_profile.html')            
        
        if address and address != user.address:
            user.address = address

        if phone and phone != user.phone:
            user.phone = phone

        db.session.commit()
        flash('Dados atualizados com sucesso!', 'success')
        return redirect(url_for('auth.update_profile'))

    return render_template('my_profile.html')

@auth.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@auth.route('/Admin_Dashboard')
@login_required
def adm_Dashboard():
    if not current_user.admin:
        flash('Somente o administrador pode acessar esta página.', category='danger') 
        return redirect(url_for('auth.products'))
    
    users = User.query.all()
    products = Product.query.all()
    return render_template('showdata.html', users=users, products=products)

@auth.route('/admin/add_default_products', methods=['GET', 'POST'])
def adicionar_produtos_padrao():
    produtos = [
        {
            'name': 'BOLO DE CHOCOLATE LAR DAS CRIANÇAS 85 ANOS',
            'price': 215,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_de_chocolate_lar_das_criancas_85_anos_1175_1_0fef3fc16a8055abbe2260d5d1411c9e.jpg',
            'description': 'Criamos um bolo exclusivamente para contribuir com uma causa que nos é muito querida. Você compra este bolo e 15% da renda será doada para o Lar da Criança da CIP, que neste ano completa 85 anos de existência.'
        },
        {
            'name': 'MONTE SEU BOLO',
            'price': 250,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/monte_seu_bolo_847_1_01926eac43814a7a652c1ee302109e88.png',
            'description': 'Agora você pode montar seu bolo com o sabor da massa, recheios e cobertura que desejar. Prepararemos tudo com muito cuidado e carinho para você receber o seu bolo, do jeitinho que você quer.'
        },
        {
            'name': 'BOLO DE MEL NO PRATO JAY',
            'price': 85,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_de_mel_no_prato_jay_945_1_591ab7fbb63b643cc2fdb51ad385bc44.jpg',
            'description': 'Nosso tradicional bolo de mel é feito com puro mel de abelhas, suco de laranja,  especiarias e uma calda fondant que finaliza e deixa tudo mais docinho e saboroso..'
        },
        {
            'name': 'BOLO INTENSIVE CHOCOLATE FLOURLESS',
            'price': 280,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/intensive_chocolate_flourless_cake_779_1_4a5daec065980d9ff2b888cf41846e32.jpg',
            'description': 'Este bolo de chocolate e amêndoas polvilhado com cacau é ideal para quem está evitando açúcar, glúten e a cozinha! A massa é assada com perfeição. Feita com farinha de amêndoas e chocolate belga 54%, caprichamos no preparo deste bolo.Cobrimos este bolo com uma calda cremosa de chocolate belga e polvilhamos com cacau. Você pode escolher somente o bolo ou o bolo embalado em uma lata linda e exclusiva da Sucrier. Um presente super especial.'
        },
        {
            'name': 'SHANA TOVÁ BOLO DE MEL RECHEADO',
            'price': 340,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_de_mel_shana_tova_583_1_5217f6004c92c6929e8349c90e039c1a.png',
            'description': 'Criamos, com muito carinho, uma receita especial e exclusiva para a coleção de Rosh Hashaná 2023. Finíssimas camadas de nosso tradicional bolo com puro mel de abelhas recheadas com um cremoso frosting de cream cheese. Delicioso!.'
        },
        {
            'name': 'BOLO CASEIRINHO DE COCO',
            'price': 215,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_caseirinho_de_coco_637_1_646cff546493555c535163b719a13127.jpg',
            'description': 'Um bolo que nos remete ao lar, aos momentos em família e encontros com amigos queridos. Nosso caseirinho de coco é feito com camadas finas de massa de chocolate feita com cacau belga, recheado com brigadeiro cremoso de coco e coberto com brigadeiro tradicional. Finalizamos a decoração com confeitos de chocolate e coco ralado. É uma delícia! Perfeito para levar em viagem. Fale com nossos atendentes e solicite o bolo já congelado.'
        },
        {
            'name': 'PRATO JÁY COM BOLO CASEIRINHO SUCRIER',
            'price': 470,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/prato_jay_com_bolo_caseirinho_sucrier_751_1_5e04cca3d414587a772425f6f8160882.jpg',
            'description': 'O bolo caseirinho da Sucrier é um clássico! Um bolo de brigadeiro bem molhadinho, preparado com cacau belga que deixa este bolo com um sabor leve e doce na medida certa. Seu sabor, aroma e texturas são inesquecíveis. Nesta versão, o bolo caseirinho da Sucrier torna-se um presente especial: vem sobre um lindo prato de cerâmica da Jáy, decorado com cogumelos. É um charme! É um presente gracioso que combina a experiência de degustar um bolo delicioso de brigadeiro com a sensação agradável de apreciar uma linda peça de cerâmica.'
        },
        {
            'name': 'BOLO PISTACHIO',
            'price': 215,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_de_limao_571_1_e162baae67c4ff04eb5424bfd34f5d1c.jpg',
            'description': 'O bolo Pistachio da Sucrier é especial. A massa é de pistache e bem fofinha, tem um recheio super cremoso de brigadeiro de pistache e é coberta com um ganache delicioso também de pistache. É docinho e delicioso! Bolo confeitado, feito à mão!'
        },
        {
            'name': 'BOLO DE LIMÃO',
            'price': 215,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_de_limao_571_1_e162baae67c4ff04eb5424bfd34f5d1c.jpg',
            'description': 'Quando criamos uma receita, pensamos em oferecer memórias e emoções especiais para as pessoas. Este bolo de Limão é decorado artesanalmente com delicadas margaridas e tem um gosto azedinho de limão siciliano que nos remetem à memórias de férias de verão em família e entre amigos. É um american style frosting cake: recheado com uma ganache cremosa e frosting de limão siciliano. Para comemorar alguma data especial, para enviar como um presente surpresa para alguém querido ou para compartilhar entre família e amigos. Bolo confeitado, feito à mão!'
        },
        {
            'name': 'BOLO CARROT',
            'price': 215,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_carrot_569_1_db7439ea5b0d94fa2b5715accf79ef00.jpg',
            'description': 'Não é apenas um bolo de cenoura. É O Bolo de Cenoura que impressiona e traz felicidade. Pedacinhos de cenoura, especiarias e chocolate belga dão o toque especial à essa suculenta receita americana de carrot cake, recheada de camadas de brigadeiro bem cremoso. A cobertura é um frosting de cream cheese que equilibra e finaliza o carrot cake mais gostoso da região.'
        },
        {
            'name': 'BOLO RED VELVET',
            'price': 215,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_red_velvet_567_2_9be024d3a6d6c0ad623d2284848e1758.jpg',
            'description': 'Lindo de se ver, o bolo Red Velvet da Sucrier é uma combinação equilibrada de sabores que sempre impressiona. É um american style frosting cake - massa de red velvet com recheio de frosting de cream cheese e geléia de frutas vermelhas orgânicas super frescas. A cobertura é um frosting de cream cheese. Um deleite para os olhos e para as papilas gustativas! Bolo confeitado, feito à mão.'
        },    
        {
            'name': 'BOLO TRIPLE CHOCOLATE FUDGE',
            'price': 215,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_triple_chocolate_fudge_565_1_8f9e3ebead4745f5c7b9ecef1a623bc7.jpg',
            'description': 'Suculento e delicioso, este bolo é pura indulgência. Feito com massa de cacau, seu recheio é um ganache super cremoso de chocolate belga meio amargo. Este mesmo ganache e um caramelo com flor de sal cobrem este bolo super especial. A decoração é finalizada com algumas guloseimas bem docinhas. Doce e amargo bem equilibrados. O resultado é divino! Para os amantes de chocolate de todas as idades!'
        },
        {
            'name': 'BOLO CASEIRINHO',
            'price': 215,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_caseirinho_563_1_c392b60697b9c71fc7463f401d297f7f.jpg',
            'description': 'O bolo caseirinho da Sucrier é um bolo de brigadeiro bem molhadinho. É aquele bolo que traz à memória os momentos em família ao redor da mesa no final da tarde. Para reviver ou criar doces momentos em família, este é o bolo ideal! E é um dos preferidos das crianças.'
        },
        {
            'name': 'BOLO HEART TO HEART',
            'price': 240,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_heart_to_heart_549_1_afb07e52bd7304739bbbfc91052db283.jpg',
            'description': 'O coração é um símbolo associado à emoção e ao prazer. Com isto em mente, modelamos pequeninos e delicados corações para enfeitar um bolo criado especialmente para celebrar o amor.'
        },
        {
            'name': 'BOLO CANDY',
            'price': 215,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_candy_cake_645_1_6a6cb8a320f72803935ba991f239862d.jpg',
            'description': 'Colorido, gostoso e divertido! Um bolo para alegrar todas as crianças e muitos adultos também! Criamos esta receita inspiradas nos momentos que compartilhamos com nossos filhos e o resultado é um bolo super divertido e cheio de guloseimas para todas as idades.'
        },
        {
            'name': 'CASEIRINHO SEM GLÚTEN SEM LACTOSE',
            'price': 390,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/caseirinho_sem_gluten_sem_lactose_1314_1_b5f140fbc5a9cf7acc46d4df7e40b0ef.jpg',
            'description': 'O bolo caseirinho da Sucrier é um bolo de brigadeiro molhadinho, agora na versão mais leve sem glúten e sem lactose. *Contém açúcar. Feito com chocolate 70%, povilhamos cacau e na lateral confeitos amargo é ideal para quem está evitando, glúten, lactose e quer comemorar momentos marcantes. Um presente super especial.'
        },
        {
            'name': 'BROWNIE OU BLONDIE',
            'price': 190,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/brownie_ou_blondie_na_lata_1057_1_e86b4ddf833d49c1fce2a75255ad85d3.jpg',
            'description': 'O Blondie é um Brownie diferente. Não leva o açúcar refinado em sua receita. É feito com açúcar mascavo e chocolate branco e tem um gostinho de caramelo. Nosso Brownie é feito com muiiitooo chocolate belga meio amargo. O brownie é super gostoso e feito com muito carinho pela Sucrier.'
        },
        {
            'name': 'BOLO DE MEL',
            'price': 190,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_de_mel_873_1_e6c7a0aaeeed54e33f624fc1acdfc7f8.jpg',
            'description': 'O bolo de mel está presente em nossas memórias e nos dedicamos para que este bolo, fique docemente marcado em suas memórias também..'
        },
        {
            'name': 'BOLO DE COCO GELADO',
            'price': 330,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_de_coco_gelado_na_lata_783_1_b4387f338fd5cf39666f1be749dfa307.jpg',
            'description': 'Bolo de coco gelado - um clássico preparado com muito carinho e que agora vem em uma lata linda, tornando este bolo um presente especial. É macio, molhadinho, com sabor intenso de coco e é gelado! É um bolo que desperta doces memórias e uma opção de sobremesa muito pedida em nossas lojas. Facilmente se esgotam.'
        },
        {
            'name': 'BOLO FINANCIER DE PISTACHE',
            'price': 420,
            'image': 'https://images.tcdn.com.br/img/img_prod/913527/bolo_financier_de_pistache_na_lata_781_1_4280e6febebac668199acc0612648261.jpg',
            'description': 'A Sucrier se dedica para que você proporcione doces emoções para quem você ama. Com isto em mente, desenvolvemos um novo sabor de bolo: um financier de pistache e o colocamos em uma lata linda!.  Acrescentamos ao financier - um clássico da cozinha Francesa, feito com farinha de amêndoas - um toque de pistache, criando uma combinação perfeita de sabores. O bolo fica bem suave e molhadinho. A farinha de amêndoas deixa a massa úmida e cheirosa, e o pistache, combinado com as amêndoas, deixa aquele docinho suave na boca a cada pedaço. .'
        }
    ]
    

    for produto in produtos:
        novo_produto = Product(
            name=produto['name'],
            price=produto['price'],
            image=produto['image'],
            description=produto['description']
        )
        db.session.add(novo_produto)  # Adiciona o produto na sessão do banco
    db.session.commit()  # Salva as mudanças no banco de dados

    flash('Produtos adicionados com sucesso!', 'success')
    return redirect(url_for('auth.adm_Dashboard'))

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
        flash('Somente o administrador pode acessar esta página.', category='danger') 
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
        flash('Somente o administrador pode acessar esta página.', category='danger') 
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
    if current_user.admin:
        flash('Somente clientes podem acessar essa página.', 'danger')
        return redirect(url_for('auth.home'))
    
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

@auth.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    OrderItem.query.filter_by(order_id=order.id).delete()
    db.session.delete(order) 
    db.session.commit() 

    flash('Pedido excluído com sucesso!', 'success')
    return redirect(url_for('auth.admin_orders'))  