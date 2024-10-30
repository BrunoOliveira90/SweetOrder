from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required
from app import db
from app.models import Order, OrderItem, Product, User

admin = Blueprint('admin', __name__)

@admin.route('/painel_do_admin')
@login_required
def adm_Dashboard():
    if not current_user.admin:
        flash('Somente o administrador pode acessar esta página.', category='danger') 
        return redirect(url_for('client.products'))
    
    users = User.query.all()
    products = Product.query.all()
    return render_template('admin/dashboard.html', users=users, products=products)

@admin.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    if not current_user.admin:
        flash('Acesso negado. Apenas administradores podem alterar o status dos pedidos.', 'danger')
        return redirect(url_for('admin.admin_orders'))

    order = Order.query.get_or_404(order_id)
    
    new_status = request.form.get('status')

    if new_status:
        order.status = new_status
        db.session.commit()
        flash(f'Status do pedido #{order.id} atualizado para {new_status}', 'success')
    else:
        flash('Selecione um status válido.', 'danger')

    return redirect(url_for('admin.admin_orders'))


@admin.route('/adicionar_produto', methods=['GET', 'POST'])
@login_required
def addprod():
    if not current_user.admin:
        flash('Somente o administrador pode acessar esta página.', category='danger') 
        return redirect(url_for('client.products'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        image = request.form.get('image')
        category = request.form.get('category')
        
        productname = Product.query.filter_by(name=name).first()

        if productname:
          flash('Este produto já foi registrado.', category='danger')                      
        else:
            new_product = Product(name=name, price=price, image=image, description=description, category=category)
            db.session.add(new_product)
            db.session.commit()
            flash('Produto adicionado com sucesso', category='success')
            return redirect(url_for('admin.addprod'))
    
    return render_template('admin/prod_add.html')

@admin.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
@login_required
def editprod(id): 
     if not current_user.admin:
        flash('Somente o administrador pode acessar esta página.', category='danger') 
        return redirect(url_for('client.products'))
     
     product = Product.query.get(id)

     if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = request.form.get('price')
        product.description = request.form.get('description')
        product.category = request.form.get('category')

        db.session.commit()
        flash('Produto atualizado com sucesso', category='success')
        return redirect(url_for('admin.editprod', id=product.id))

     return render_template('admin/prod_edit.html', product=product)

@admin.route('/Delete_Product/<int:id>', methods=['POST'])
@login_required
def delprod(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    flash('Produto removido com sucesso', category='success')
    return redirect(url_for('client.products'))

@admin.route('/admin/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('admin.adm_Dashboard'))


@admin.route('/admin_pedidos')
@login_required
def admin_orders():
    if not current_user.admin:
        flash('Apenas administradores podem acessar essa página.', category='danger')
        return redirect(url_for('client.products'))
    
    orders = Order.query.all()
    return render_template('admin/admin_orders.html', orders=orders)

@admin.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    OrderItem.query.filter_by(order_id=order.id).delete()
    db.session.delete(order) 
    db.session.commit() 

    flash('Pedido excluído com sucesso!', 'success')
    return redirect(url_for('admin.admin_orders'))  


@admin.route('/admin/add_default_products', methods=['GET', 'POST'])
def adicionar_produtos_padrao():
    produtos = [
        {
            'name': 'BOLO PERSONALIZADO - UNICÓRNIO',
            'price': 149,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczP3PAGe48er_yBhXofPUoCpDEy4b83maqrb3hSIAwCzrldrxhTBtVZ4iUT0jI3y5zx8_CPlCm0Cb2bmS0e3ZRbAtdsx7hYLLroPjSXUCcpWqbfuFR2CVqRrO36NsqqyLJhzz8Y1ktiARwqKhcQ0UHvMXw=w694-h925-s-no-gm?authuser=2',
            'description': 'Bolo decorado para festas infantis - Consulte-nos para encomendar o seu tema.',
            'category': 'aniver'
        },
        {
            'name': 'BOLO PERSONALIZADO - FESTA JUNINA',
            'price': 149,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczMZ43lAJbW3zu7X9WAyUzKecvUNnLHZEXQyIDBSqQsbn8RSKFRkK1fxNEKUcAeaI1rxXGg-jIdlmPVsYND3XRe7bl-THpt8aP-YMZPqa9tJETu0b_chmIJyFI6Gv0e93EqpfRCLBd_rWQAZOuMKO0ElmQ=w694-h925-s-no-gm?authuser=2',
            'description': 'Bolo decorado temático para festas típicas - Consulte-nos para encomendar o seu tema.',
            'category': 'bolos'
        },
        {
            'name': 'BOLO RECHEADO DECORADO',
            'price': 189,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczMAsGla08h9ezxQkgJLFiRtRvd5ROVxJmQaKYT0RMI4xpUZAELIZECyskIJwDqc9RlsNpw1nkY36dUzDZAtqA8zsN8o6qBpARPZM3e1rTVVb2MLYsAYHk-hHSeCTnnZh5IRhJ-UPLFFssNzv7S8Bg5NIQ=w1233-h925-s-no-gm?authuser=2',
            'description': 'Bolo decorado com recheio personalizado - Consulte-nos para encomendar do seu jeito.',
            'category': 'bolos'
        },
        {
            'name': 'BOLO NAKED - KINDER COM MORANGO',
            'price': 179,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczNg4OgVugq34rjn_REg4ijMWIs_Q28MkVj2X_i-uXP0wWyR40JFjLurJijTut9OOfTSNaNzkgCP6-dnixeivTnLyLiSoyFtU9sxKiMcCUCVhJs3IypkD6rWqDMz5RcigtGdwEBdfq8nnl7ornxjqR7xGg=w783-h925-s-no-gm?authuser=2',
            'description': 'Bolo Naked sabor Kinder Ovo, recheado com ganache e morango - Consulte-nos para encomendar do seu jeito.',
            'category': 'bolos'
        },
        {
            'name': 'BOLO RECHEADO - KINDER BUENO',
            'price': 199,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczMQOep6AsCo0l2gCWEdUL2oeyID-ycoZOYqzM9cn_ealKSUSVWwJDf04rEPXOFBf_T4W6gKB73TuI9cSI1v9eI_e7D-Pyc35tGZcWGpTZxsrX8YvEH6-C5CPBz2i3lmtlC8k8kEdGxZGXBLhcVtcRmH4A=w745-h925-s-no-gm?authuser=2',
            'description': 'Bolo Recheado sabor Kinder Bueno, com brigadeiro - Consulte-nos para encomendar do seu jeito.',
            'category': 'bolos'
        },
        {
            'name': 'BOLO PERSONALIZADO - PASTA AMERICANA',
            'price': 219,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczNaPWMQZmYoiilgyRhwuyNQK6Qd7ZDtTWL0JqGmrFp-Ep_TPQ7WtTHao5iTajtDIrif5SrY7fUgZwoeAnAIilCT64xXdQ69kGrPJg06QqiBYuqrV90qsWjPKXM5VSggwNkZpcW93rzOj6KAaHuBFVlbpg=w873-h925-s-no-gm?authuser=2',
            'description': 'Bolo personalizado para festas infantis com Pasta Americana - Consulte-nos para encomendar do seu jeito.',
            'category': 'aniver'
        },
        {
            'name': 'BOLO PERSONALIZADO - FLURK 2kg',
            'price': 99,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczNsCXVhzWKRFiMV2bXRh0Zzx9FBqqCA5qIUBSh7j3yjM8i_3p893Y_bh48cjXMXHBAkYk2an06X7mO1hBWxAtIPpzpgcwaTM3gSSajHKJZDsmaYoFIqs5n-hxES8qsbAATo9zzaQKJUQNo2viSzl-drww=w792-h925-s-no-gm?authuser=2',
            'description': 'Bolo personalizado estilo Flurk - Consulte-nos para encomendar do seu jeito.',
            'category': 'aniver'
        },
        {
            'name': 'BOLO PERSONALIZADO - FLURK 1kg',
            'price': 59,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczO-XBE5VfZCSVfxlOnb11k0YxPyASVz6ZtL2voUI9cVHEWIhyWlplGTJlWGYDfA24V6ycMG8hfUo278noep-j4NWIp20faektBOFiiTjsZFJdbhiR9cXP-Q7tyDI40kVivasL6pFlewK_-Uv5Pqcposww=w755-h925-s-no-gm?authuser=2',
            'description': 'Bolo personalizado estilo Flurk - Consulte-nos para encomendar do seu jeito..',
            'category': 'aniver'
        },
        {
            'name': 'BOLO PERSONALIZADO - ARTÍSTICO',
            'price': 279,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczPwcxi0aCfzK41c-Qb2Bw4CmMa4w0iiPLkOmPsgi3u5JXr3aFRN2zB1U1Kdsds7gcsg3h5QsUj3lOuNf8Ka3xwEENtH06kWQQIkqaDBaYZRXJQz5_soye-D9sOmYjZ-q_Kd3zBQS1v-fH1qcUdiD4RFFQ=w925-h925-s-no-gm?authuser=2',
            'description': 'Bolo personalizado artístico - Consulte-nos para encomendar do seu jeito.',
            'category': 'bolos'
        },
        {
            'name': 'MINI BOLO RECHEADO DECORADO',
            'price': 89,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczMUC2cT-O1cL_EWbBAPpjgPN1nOdVByaph8wIlXqBNLlolqm4G6mi2ephJZOItpwKyct0b_qgq0JC55DsXd5VlSCvJj_SsWzMKTOENv0UMBx1i20dN2Ow8bqcy0ZY3JrlrocIV-h54-IZIfJDdm7K4Usw=w925-h925-s-no-gm?authuser=2',
            'description': 'Bolo recheado de 1kg - Consulte-nos para encomendar do seu jeito.',
            'category': 'bolos'
        },
        {
            'name': 'BOLO PERSONALIZADO - SORVETE',
            'price': 119,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczMwglT2ky0n88OmXisqD7keYl1nWB6Wu3A_P-bmx1fLqzfD9FSFFxMzsalgtcmxiYboqdiPp0GNYd1Exdaeq247zpo5af7YQbJiFr2xvH3i4sWCN7VxjlKd_SHwv8-65HmCkVfLwOtXCYyHDbsQYeQYHA=w924-h925-s-no-gm?authuser=2',
            'description': 'Bolo personalizado temático - Consulte-nos para encomendar do seu jeito.',
            'category': 'aniver'
        },
        {
            'name': 'KIT BOLO DE POTE + BOMBOM',
            'price': 49,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczNGN84xsVFHU7VWmxYylu3CYUvvAI5vLwvxOvOu0DXq0ddie0dPoxmTtO1fUKVV_f_cpEGhxX89e1nEBjUIVd_kO5AI49MBF9Lzn4Cm6pXYzVURl63jW8ljDA2mnr-bY9MGLMTP_MRvG1V5dB_xIoAhrA=w925-h925-s-no-gm?authuser=2',
            'description': 'Kit com 4 un. sendo 2 Bolos de pote, 1 bombom e 1 brownie - Consulte-nos para encomendar do seu jeito.',
            'category': 'bolosdepote'
        },
        {
            'name': 'BOLO DE POTE RECHEADO - SABORES',
            'price': 29,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczPdzw8od0pUvhGl4Z_W7DWBFK5n7LsogZoYSIKsBB_CDABQOEp-iT95xkkrgH6ZS_HDcPQGDPh-0Lwv8tD76RW8HaSEiFGlMX9hlQ7yOIt_P8swNw75c9sxOCfQaVhbNVOb2sLE22x4NlOeFMHpnqC48A=w756-h925-s-no-gm?authuser=2',
            'description': 'Bolo de pote recheado, diversos sabores - Consulte-nos para encomendar do seu jeito.',
            'category': 'bolosdepote'
        },
        {
            'name': 'BOLO DE POTE RECHEADO - FRUTAS',
            'price': 29,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczP_qPb2hOz3bhn_FaZkFTb9LsTcQajIouTyTIBjGuJy5txyvFYxTUMrKy2dOJeYlrsFdE1mr2dpG4QnnwBhaIPxubs2oDY_py3K90eNb3Y2vpCO6Mc9gSWJmOqxy0GJKlmh5f8EZca1v_Vp8d3XMqXerg=w740-h925-s-no-gm?authuser=2',
            'description': 'Bolo de pote recheado, diversos sabores - Consulte-nos para encomendar do seu jeito.',
            'category': 'bolosdepote'
        },
        {
            'name': 'BOLO DE POTE RECHEADO - PEQ.',
            'price': 19,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczNBchZNGAJlKj-W7YrgK9Wut8fLt152gEXXxVyZDq05eeFskWJVMQ8QrDkHeSCPh7vavjLnBYM7qwuXPkX7YXNuljrBI5DKEAna8ayu1RQgbn61Xwoyhhp1QDr81nktC4ztB9LTJhR3SEF3oosMpJaSwg=w824-h925-s-no-gm?authuser=2',
            'description': 'Bolo de pote pequeno, diversos sabores - Consulte-nos para encomendar do seu jeito.',
            'category': 'bolosdepote'
        },
        {
            'name': 'BOLO DE TAÇA RECHEADO - MORANGO',
            'price': 69,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczPy8TZbdN1iAi9bdJWHQ-FbLYQZhGWzCCbNkTRX7IVeuQR7gYNbFVwilIiej_MCMgk0nPLucUEFP9CQV6qWTgsgt2ZxusEOb83g6Tfmm3dnUhrAvlQgvF16Uf9FlgEcSlJZbXbvc4FIrjgtOAALHAH31w=w837-h925-s-no-gm?authuser=2',
            'description': 'Bolo de Taça, diversos sabores - Consulte-nos para encomendar do seu jeito.',
            'category': 'bolosdepote'
        },
        {
            'name': 'BOLO DE TAÇA RECHEADO - LEITE NINHO COM NUTELLA',
            'price': 69,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczO7tNVDrzH-AUtCvAzT1SWbzsEtA3ohMUyjLvFd8fiArDmqvC5qs0wSWfPY0TYNDBXQ764jZOEHuooH7KwNCUybSCjptNVWy3MFEaSGJYbrtqMJ1oCQ5T4gOP1E_kqvEZI43QK8a_6P8Um2ebhyVWRFgA=w739-h925-s-no-gm?authuser=2',
            'description': 'Bolo de Taça, diversos sabores - Consulte-nos para encomendar do seu jeito.',
            'category': 'bolosdepote'
        },
        {
            'name': 'BOLO TE TAÇA RECHEADO - UVA',
            'price': 69,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczNNA3RQ2YACrnVM7YMkXG_Zq_HCU11FWY3vxYcFjnTTGdQ1_XvRXlH2tGo5sTnooeQ0-thTzwZ7i4buyp2XMMj1Lifjf-hOPSLNgoplwblETAXjICWtl2xcVQq073JKSmOQYzDvLdn8gKvrMJRdJNsHBQ=w909-h925-s-no-gm?authuser=2',
            'description': 'Bolo de Taça, diversos sabores - Consulte-nos para encomendar do seu jeito.',
            'category': 'bolosdepote'
        },
        {
            'name': 'BOMBONS ESPECIAIS - CAIXA',
            'price': 79,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczMnYhnhmPOfYRuDenXPsHiM2QnEKhibU4jKyY9VTmiWW3ZEhKu84jkP3BdY0xXNibJmNFWUqooYCbvDR0KKbZDmDJJsZJ-rxtgt7MgfxWoG0zJQNVpeaxcvHolYxln5ZLVUOip2YL4-_GXAfTVtIMOX3Q=w925-h925-s-no-gm?authuser=2',
            'description': 'Bombons de morango trufado, 15 unidades.',
            'category': 'docinhos'
        },
        {
            'name': 'CENTO DE DOCES GOURMET',
            'price': 99,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczN-5Rmv464ihyJduj70d85drQkJ8qTsNmwUsE294Cn9MJmNmgbqSMpIX2zaaDNADqrUeMI4As-8jDUO7ZT_yaeWe3S0nGZN-oheF3uEeL_V1Hd1mIo0nl5G3X3mUApq95PZMyvxwagTVeW9WIwW1CXa5g=w925-h925-s-no-gm?authuser=2',
            'description': 'Cento de doces Gourmet - Consulte-nos para encomendar do seu jeito.',
            'category': 'docinhos'
        },
        {
            'name': 'CENTO DE DOCES - BEIJINHO',
            'price': 49,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczOTj7rPH6Gv5ROCTda4hVVH5ZpuGDASIi1e7QAhf9R8vrpW9887OT3DS7xA8CPXb0BJd5Es2gqfMLT05-AzFbAEjJyjPCMZIEg5In_U0bEKSKFGcDSUcGrq6C8PJlKWt98czEAp7I3fzs__3EcQfUVPmw=w925-h925-s-no-gm?authuser=2',
            'description': 'Cento de doces Gourmet - Consulte-nos para encomendar do seu jeito.',
            'category': 'docinhos'
        },
        {
            'name': 'CENTO DE DOCES - CHURROS',
            'price': 49,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczO4IqrBrP0etzVTM9xMHpM2zHUCXL-vz3FRuPtEZ8_36I5SjMLVIPSK3DVJatdRPwfAhCwLOPGn89DCwE9HrwbvF-nY-j2u7fztCKGvFSR7GL0xLDclQu1Fk-HDEgAHiEPLY5qV8wTqkCTTPuZjeVy8Aw=w925-h925-s-no-gm?authuser=2',
            'description': 'Cento de doces Gourmet - Consulte-nos para encomendar do seu jeito.',
            'category': 'docinhos'
        },
        {
            'name': 'CENTO DE DOCES GOURMET - MIX',
            'price': 99,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczPZrIRExpTRB0sy4bP08yNCegyxU35aTtTZdnSvAVcBGaccZF8BNYljfGXNc7ZQErPcvN13qG5w6z_aJwzleuNQIepdq0-XKfsCLxWXL1LbiFxJhwU-d36T8I5M13MTiUBUJBJNAk01SxyXJ_Dia4tGng=w925-h925-s-no-gm?authuser=2',
            'description': 'Cento de doces Gourmet - Consulte-nos para encomendar do seu jeito.',
            'category': 'docinhos'
        },
        {
            'name': 'CENTO DE DOCES - BRIGADEIRO + BEIJINHO',
            'price': 49,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczP3JUj5apKjfeAFqaTVwx0tReU_51qVbinNnXsXUtKf4G8_BaJ9B0ohLydwP1b9mZTmX44epLFKCb4zSPJ3FUegFZ9TrroiYE8q1JJzlt5BokLU7sAVAiLzVDMsqEou9z4k3i6BYKuK8m1LFIVTea8l4g=w925-h925-s-no-gm?authuser=2',
            'description': 'Cento de doces Gourmet - Consulte-nos para encomendar do seu jeito.',
            'category': 'docinhos'
        },
        {
            'name': 'PANETONE ESPECIAL DE NATAL',
            'price': 99,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczNhkTUb5NTsqnG3_nZbLbBkXy2Ql5k-1APpVT37Q56e8olAd8E7oaKyZHo1D_MW_MzxLlVGrViEMFeQuP-ASOrCODfexUJ2MyEaVuRTaMcbWSAOcEcbvy3022HpwYyFNFYGmp7MTJF_KCfMdWm4m-JWag=w925-h925-s-no-gm?authuser=2',
            'description': 'Panetone especial de Natal, diversos sabores - Consulte-nos para encomendar do seu jeito.',
            'category': 'natal'
        },
        {
            'name': 'OVO DE PÁSCOA DE COLHER - 2un',
            'price': 99,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczM_8NlTiGGLpbkwBg1Sv-p_yl0TtGv9zHRhvZfwLx0G1yBqRLHNf361wmS_C6d9N3_PQ6b7p0ZX5A98XKiqt8aaTHOxx59FQm6Zk7sagW1XbXaWlN2XtmssJSGd0Qe4QJKWohTk_prESeud_I89fvOpbw=w925-h925-s-no-gm?authuser=2',
            'description': 'Ovo de páscoa recheado, diversos sabores₢ - Consulte-nos para encomendar do seu jeito.',
            'category': 'pascoa'
        },
        {
            'name': 'OVO DE PÁSCOA DE COLHER - MORANGO 1un',
            'price': 69,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczOMNo_qPnEhVOY6yJtEH4OwuGHsYE-SrAbYZsUYY1XFQZfBXrgF9E5zfklvp54Gaegi9IFJ-AzRT6l6ozlhhjL7jRoYtKiaifhr9zQR6t91McVIVQYS5spxiAHydw-KG9b0pK7I_F2q4mPN_cnM_35TNQ=w960-h640-s-no-gm?authuser=2',
            'description': 'Ovo de páscoa recheado, diversos sabores₢ - Consulte-nos para encomendar do seu jeito.',
            'category': 'pascoa'
        },
        {
            'name': 'OVOS DE PÁSCOA DE COLHER - 4un',
            'price': 79,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczOdc_3P72dCr_YoL4BBMjkiuZfGsqanVcDcbQeQ_A62BwsYLdOTFwIqyqH3ltd5RMHJvNanupO2aie-2gPXHVGJwmNsz34RpwahOfkaFxWAyMKBihuBQPKJc4sUCH406rV-49ViGJiUi4K75wm3QhGSMQ=w960-h640-s-no-gm?authuser=2',
            'description': 'Ovo de páscoa recheado, diversos sabores₢ - Consulte-nos para encomendar do seu jeito.',
            'category': 'pascoa'
        },
        {
            'name': 'OVOS DE PÁSCOA DE COLHER - KINDER 1un',
            'price': 69,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczOFFXQt_WDp03N6HQYvezAxzwz5lOD1qEPcqu9nlxfJyGfFtZsJv10_Oa5ZYdLO0Slv4Iyc2TRZb-rsHz1RjGYpzeYw6pH71z5QF0Nz4c_YWJNbEFP3btTdTsfPTKRHoyTO7DTkO1ZcE_KIf594LkDhXQ=w960-h636-s-no-gm?authuser=2',
            'description': 'Ovo de páscoa recheado, diversos sabores₢ - Consulte-nos para encomendar do seu jeito.',
            'category': 'pascoa'
        },
        {
            'name': 'OVOS DE PÁSCOA DE COLHER - DOIS AMORES 2un',
            'price': 79,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczO2lpWqOeFd3lC5q_OkSlXVNiozqLGeZnQtfLH9XoLplpboPi52p1RSMSxv6NY0yDYPiiepOOOr6oh-tWeOXMZRfiZdns_DRQy8bz7Uuc7pMQKvinl2M4Cr3ydrdVchKF2zHWgLqec03GMxxjXgtIUu9g=w960-h636-s-no-gm?authuser=2',
            'description': 'Ovo de páscoa recheado, diversos sabores₢ - Consulte-nos para encomendar do seu jeito.',
            'category': 'pascoa'
        },
        {
            'name': 'OVOS DE PÁSCOA DE COLHER - MISTO 2un',
            'price': 79,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczOgCPWOEWqYAdDqVG7LZAMp3t3Rjq9rHtLW97itU7buzZ4CUL0YioK7i8WzraRWyMb_FC2kfp0L7ReAUGvgtou4Lb8Bd3b3Oms9WZMnXvvu8K9yDqCohn5e64VDUL3knvfVoViOwZC1LN_mhSQItC8OIA=w934-h925-s-no-gm?authuser=2',
            'description': 'Ovo de páscoa recheado, diversos sabores₢ - Consulte-nos para encomendar do seu jeito.',
            'category': 'pascoa'
        },
        {
            'name': 'BOLO DE ANIVERSÁRIO - PERSONALIZADO',
            'price': 99,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczNoR0ah_YtfV5rlVLvPFLn-cVYOyTSzEaheXvvgP-CtyQmdP-spMgyt7o6hAiq3PYMRRw_-6PELTyr52FfrTFXy8fDIcvFBKmH8BUj5dkkd-vouES6nj80zJdSa52JUwDcqnyfj162WazDQHpr43ItkwQ=w925-h925-s-no-gm?authuser=2',
            'description': 'Bolo personalizado temático - Consulte-nos para encomendar do seu jeito.',
            'category': 'aniver'
        },
        {
            'name': 'PANETONE ESPECIAL DE NATAL - NUTELLA',
            'price': 99,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczNY9ZXqKi0XY1OSLnWW-WtRkkl-FIYsgvYuYHAcCUuMiKQJ52YejYsQEp-ugsBX2K_1I8tPRWfkA758pfHUCPFHVNPNk_cIlJhG-BOtkGaYzL3QqWmaAe4-GWnT967s8uq0hMIihRj_YlifAuqhZ9aXrg=w925-h925-s-no-gm?authuser=2',
            'description': 'Panetone especial de Natal, diversos sabores - Consulte-nos para encomendar do seu jeito.',
            'category': 'natal'
        },
        {
            'name': 'PANETONE ESPECIAL DE NATAL - SABORES',
            'price': 99,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczOsrDlyfG2dd6QgcjTvOKjRQiyjThuJCvL9A5ZfuP571yJSS9Uz_AbgAer2ZO-2JAnHNQMddQwMm_TfCGk7iEgsLJdrdzgIinaAK2lpMp2Npb7BfV0TBOpmT8k6fgVPozfQdQf-mxbgLV3QRkR_bx5AHA=w925-h925-s-no-gm?authuser=2',
            'description': 'Panetone especial de Natal, diversos sabores - Consulte-nos para encomendar do seu jeito.',
            'category': 'natal'
        },
        {
            'name': 'PANETONE ESPECIAL DE NATAL - SABORES',
            'price': 99,
            'image': 'https://lh3.googleusercontent.com/pw/AP1GczO-7_tNWOxItvP6YMyQKiB0WwhL0xNwK2IO-4uI6WsQv0FnuZ6tTwFl8ir2TrO5izzxDHQ04jQFnG2oSJHF2M9SIuz2gpLQWnyuPQWnbQn_5bXS2EJ25APoqwuRnXx392jE-ZatSvGsIpuF0YPPDbyKzQ=w925-h925-s-no-gm?authuser=2',
            'description': 'Panetone especial de Natal, diversos sabores - Consulte-nos para encomendar do seu jeito.',
            'category': 'natal'
        }


    ]
    

    for produto in produtos:
        novo_produto = Product(
            name=produto['name'],
            price=produto['price'],
            image=produto['image'],
            description=produto['description'],
            category=produto['category']
        )
        db.session.add(novo_produto)  
    db.session.commit() 

    flash('Produtos adicionados com sucesso!', 'success')
    return redirect(url_for('admin.adm_Dashboard'))
