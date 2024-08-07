from peewee import Model, CharField, TextField, IntegerField, ForeignKeyField, DateTimeField, BooleanField, SqliteDatabase
from playhouse.sqlite_ext import SqliteExtDatabase
from werkzeug.security import generate_password_hash

db = SqliteExtDatabase('sweetorder.db')

class BaseModel(Model):
    class Meta:
        database = db
class User(BaseModel):
    email = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)

    @classmethod
    def create_user(cls, email, password, is_admin=False):
        hashed_password = generate_password_hash(password)
        return cls.create(email=email, password=hashed_password, is_admin=is_admin)

class Product(BaseModel):
    name = CharField()
    description = CharField()
    price = CharField()
    image_url = CharField()

class Order(BaseModel):
    user = CharField()
    status = CharField()
    created_at = CharField()

class OrderItem(BaseModel):
    order = CharField()
    product = CharField()
    quantity = CharField()

def initialize_db():
    db.connect()
    db.create_tables([User, Product, Order, OrderItem], safe=True)
    db.close()