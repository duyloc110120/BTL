import json
from Bookstore import app, db
from Bookstore.models import User, UserRole, Product, Category
from sqlalchemy import func
from sqlalchemy.sql import extract
from flask_login import current_user
import hashlib


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def read_data(path='data/categories.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def load_categories():
    return Category.query.all()
    # return read_json(os.path.join(app.root_path, 'data/categories.json'))


def load_products(cate_id=None, kw=None, from_price=None, to_price=None, page=1):
    products = Product.query.filter(Product.active.__eq__(True))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if kw:
        products = products.filter(Product.name.contains(kw))

    if from_price:
        products = products.filter(Product.price.__ge__(from_price))

    if to_price:
        products = products.filter(Product.price.__le__(to_price))

    return products.all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def create_user(name, username, password, email=None, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=email.strip() if email else email,
                avatar=avatar)
    db.session.add(user)

    try:
        db.session.commit()
    except:
        return False
    else:
        return True


def check_user(username, password, role=UserRole.USER):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                             User.user_role.__eq__(role)).first()
