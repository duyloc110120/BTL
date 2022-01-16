import json
import os

from Bookstore import app, db
from Bookstore.models import User, UserRole, Product, Category, Receipt, ReceiptDetail
from sqlalchemy import func
from sqlalchemy.sql import extract
from flask_login import current_user
import hashlib


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


# def read_data(path='data/categories.json'):
#     with open(path, encoding='utf-8') as f:
#         return json.load(f)


def load_categories():
    return Category.query.all()
    # return read_json(os.path.join(app.root_path, 'data/categories.json'))


# def load_products(path='data/products.json'):
#     with open(path, encoding='utf-8') as f:
#         return json.load(f)


def load_products(cate_id=None, kw=None, from_price=None, to_price=None):
    products = Product.query.filter(Product.active.__eq__(True))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if kw:
        products = products.filter(Product.name.contains(kw))

    if from_price and to_price:
        products = products.filter(Product.price.__gt__(from_price),
                                   Product.price.__lt__(to_price))

    return products.all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def load_receipt(receipt_id):
    receipt = Receipt.query.filter(receipt_id)

    return receipt.all()


def create_user(name, username, password, email=None, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                avatar=avatar,
                user_role=UserRole.USER)
    db.session.add(user)

    try:
        db.session.commit()
    except:
        return False
    else:
        return True


def update_book(name, quantity):
    name = Product.query.filter(Product.name.__eq__(name.strip()))
    if name:
        quantity_1 = name.filter(Product.quantity.__eq__(quantity))
        quantity = Product(quantity=quantity + quantity_1)

        db.session.add(quantity)

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


def cart_stats(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }


def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
            detail = ReceiptDetail(receipt=receipt,
                                   product_id=c['id'],
                                   quantity=c['quantity'],
                                   price=c['price'])
            db.session.add(detail)

        db.session.commit()


def cate_stats():
    return Category.query.join(Product,
                               Product.category_id.__eq__(Category.id),
                               isouter=True) \
        .add_columns(func.count(Product.id)) \
        .group_by(Category.id, Category.name).all()


# def cate_stats2():
#     return db.session.query(Category.id, Category.name, func.count(Product.id)) \
#         .join(Product, Product.category_id.__eq__(Category.id), isouter=True) \
#         .group_by(Category.id, Category.name).all()


def product_stats(kw=None, from_date=None, to_date=None):
    q = db.session.query(Product.id, Product.name,
                         func.sum(ReceiptDetail.quantity * ReceiptDetail.price)) \
        .join(ReceiptDetail,
              ReceiptDetail.product_id.__eq__(Product.id), isouter=True) \
        .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id)) \
        .group_by(Product.id, Product.name)

    if kw:
        q = q.filter(Product.name.contains(kw))

    if from_date:
        q = q.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        q = q.filter(Receipt.created_date.__le__(to_date))

    return q.all()


def product_month_stats(year):
    return db.session.query(extract('month', Receipt.created_date),
                            func.sum(ReceiptDetail.quantity * ReceiptDetail.price)) \
        .join(ReceiptDetail, ReceiptDetail.receipt_id.__eq__(Receipt.id)) \
        .filter(extract('year', Receipt.created_date) == year) \
        .group_by(extract('month', Receipt.created_date)) \
        .order_by(extract('month', Receipt.created_date)) \
        .all()


def input_book(product_id):
    product = Product.query.filter(Product.id == product_id)
