from peewee import IntegrityError
from app.models import User, initialize_db
from werkzeug.security import generate_password_hash

def create_admin(email, password):
    initialize_db()
    hashed_password = generate_password_hash(password)
    try:
        User.create(email=email, password=hashed_password, is_admin=True)
        print(f"Admin user {email} created successfully.")
    except IntegrityError:
        print("Error: Email already registered.")

if __name__ == "__main__":
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    create_admin(email, password)
