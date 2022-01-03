from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Bookstore import db
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class User(BaseModel, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    email = Column(String(100))
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100), default='images/avatar.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


class Category(BaseModel):
    __tableName__ = 'category'

    products = relationship('Product',
                            backref='category', lazy=True)


class Product(BaseModel):
    __tableName__ = 'product'

    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id),
                         nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    db.create_all()

    products = [{
        "id": "1",
        "name": "Lập Kế Hoạch Kinh Doanh Hiệu Quả",
        "description": "Lập Kế Hoạch Kinh Doanh Hiệu Quả",
        "price": "120000",
        "image": "images/lap-ke-hoach-kinh-doanh-hieu-qua.jpg",
        "created_date": "2015-12-12",
        "quantity": "200",
        "category_id": "1"
    }, {
        "id": "2",
        "name": "Ma Bùn Lưu Manh",
        "description": "Ma Bùn Lưu Manh",
        "price": "150000",
        "image": "images/ma-bun-luu-manh.jpg",
        "created_date": "2015-12-12",
        "quantity": "600",
        "category_id": "2"
    }, {
        "id": "3",
        "name": "Giao dịch mọi nơi , không chỉ là ngân hàng",
        "description": "Giao Dịnh mọi nơi , không chỉ là ngân hàng",
        "price": "100000",
        "image": "images/bank-4.0.jpg",
        "created_date": "2015-12-12",
        "quantity": "300",
        "category_id": "3"
    }]

    for p in products:
        pro = Product(name=p['name'], price=p['price'], image=p['image'], quantity=p['quantity'],
                      created_date=p['created_date'],
                      description=p['description'], category_id=p['category_id'])
        db.session.add(pro)

    db.session.commit()
