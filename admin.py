from app import create_app, db  
from app.models import User

app = create_app()

def promover_admin(email):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            user.admin = True
            db.session.commit()
            print(f'Usuário {user.email} foi promovido a administrador.')
        else:
            print(f'Usuário com o e-mail {email} não encontrado.')

promover_admin('test3@gmail')