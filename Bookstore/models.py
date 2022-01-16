from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Bookstore import db
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    email = Column(String(100))
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100), default='images/avatar.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    __tableName__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product',
                            backref='category', lazy=True)


class Author(BaseModel):
    __tableName__ = 'author'

    name = Column(String(50), nullable=False)
    book = relationship('Product',
                        backref='author', lazy=True)


class Product(BaseModel):
    __tableName__ = 'product'

    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id),
                         nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='product', lazy=True)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=True)

    def __str__(self):
        return self.name


class Staff(BaseModel, UserMixin):
    __tableName__ = 'staff'

    name = Column(String(50), nullable=False)
    email = Column(String(100))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    debts = relationship('Debt', backref='staff', lazy=True)


class ImportReceipt(BaseModel):
    date = Column(DateTime, default=datetime.today())
    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=True)


class ImportReceiptDetail(BaseModel):
    import_id = Column(Integer, ForeignKey(ImportReceipt.id), nullable=False)
    quantity = Column(Integer, default=0)
    name = Column(String(50))
    price = Column(Integer, default=0)


class Debt(BaseModel):
    created_date = Column(DateTime, default=datetime.today())
    staff_id = Column(Integer, ForeignKey(Staff.id))
    details = relationship('OrderDetail',
                           backref='debt', lazy=True)


class OrderDetail(BaseModel):
    debt_id = Column(Integer, ForeignKey(Debt.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    quantity = Column(Integer, default=0)
    author = Column(String(50))
    category = Column(String(50))
    price = Column(Integer, default=0)


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    customer_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail',
                           backref='receipt', lazy=True)


class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)


if __name__ == '__main__':
    db.create_all()
    # categories = [{
    #     "id": 1,
    #     "name": "Sách Kinh Tế - Kĩ Năng"
    # }, {
    #     "id": 2,
    #     "name": "Sách Văn Học Việt Nam"
    # }, {
    #     "id": 3,
    #     "name": "Sách Đời Sống "
    # }, {
    #     "id": 4,
    #     "name": "Sách Thiếu Nhi"
    # }, {
    #     "id": 5,
    #     "name": "Sách Giáo Dục Gia Đình"
    # }, {
    #     "id": 6,
    #     "name": "Sách Lịch Sử"
    # }, {
    #     "id": 7,
    #     "name": "Sách Văn Hóa Nghệ Thuật"
    # }, {
    #     "id": 8,
    #     "name": "Sách Khoa Học - Triết Học"
    # }, {
    #     "id": 9,
    #     "name": "Sách Tâm Linh Tôn Giáo"
    # }, {
    #     "id": 10,
    #     "name": "Sách Y học- Thực Dưỡng"
    # }]
    #
    # for c in categories:
    #     cate = Category(id=c['id'], name=c['name'])
    #     db.session.add(cate)
    #
    # db.session.commit()

    # authors = [{
    #     "id": 1,
    #     "name": "Max"
    # }, {
    #     "id": 2,
    #     "name": "John"
    # }, {
    #     "id": 3,
    #     "name": "Kid"
    # }]
    #
    # for a in authors:
    #     author = Author(id=a['id'], name=a['name'])
    #     db.session.add(author)
    #
    # db.session.commit()

    # products = [{
    #     "id": 1,
    #     "name": "Lập Kế Hoạch Kinh Doanh Hiệu Quả",
    #     "description": "Lập Kế Hoạch Kinh Doanh Hiệu Quả",
    #     "price": 120000,
    #     "image": "images/lap-ke-hoach-kinh-doanh-hieu-qua.jpg",
    #     "created_date": "2017-12-12",
    #     "quantity": 200,
    #     "category_id": 1,
    #     "author_id": 1
    # }, {
    #     "id": 2,
    #     "name": "Ma Bùn Lưu Manh",
    #     "description": "Ma Bùn Lưu Manh",
    #     "price": 150000,
    #     "image": "images/ma-bun-luu-manh.jpg",
    #     "created_date": "2015-12-12",
    #     "quantity": 600,
    #     "category_id": 2,
    #     "author_id": 2
    # }, {
    #     "id": 3,
    #     "name": "Giao dịch mọi nơi , không chỉ là ngân hàng",
    #     "description": "Giao Dịnh mọi nơi , không chỉ là ngân hàng",
    #     "price": 100000,
    #     "image": "images/bank-4.0.jpg",
    #     "created_date": "2018-01-12",
    #     "quantity": 300,
    #     "category_id": 3,
    #     "author_id": 1
    # }, {
    #
    #     "id": 4,
    #     "name": "Bộ sách 500 câu chuyện giáo dục",
    #     "description": "Bộ sách 500 câu chuyện giáo dục",
    #     "price": 80000,
    #     "image": "images/bo-sach-500-cau-chuyen-dao-duc.jpg",
    #     "created_date": "2015-06-01",
    #     "quantity": 500,
    #     "category_id": 5,
    #     "author_id": 3
    # }, {
    #     "id": 5,
    #     "name": "Những câu chuyện về tính lương thiện",
    #     "description": "Những câu chuyện về tính lương thiện",
    #     "price": 200000,
    #     "image": "images/bo-sach-nhung-cau-chuyen-cho-con-thanh-nguoi-tu-te.jpg",
    #     "created_date": "2021-06-04",
    #     "quantity": 500,
    #     "category_id": 3,
    #     "author_id": 3
    # }, {
    #     "id": 6,
    #     "name": "Cảm ơn vì đã được thương",
    #     "description": "Cảm ơn vì đã được thương",
    #     "price": 135000,
    #     "image": "images/cam-on-vi-da-duoc-thuong.jpg",
    #     "created_date": "2021-09-04",
    #     "quantity": 500,
    #     "category_id": 3,
    #     "author_id": 2
    # }, {
    #     "id": 6,
    #     "name": "Ăn xanh sống lành ",
    #     "description": "Ăn xanh sống lành ",
    #     "price": 100000,
    #     "image": "images/combo-an-xanh-song-lanh.jpg",
    #     "created_date": "2021-06-04",
    #     "quantity": 500,
    #     "category_id": 10,
    #     "author_id": 3
    # }, {
    #     "id": 7,
    #     "name": "Buổi sáng diệu kì",
    #     "description": "Buổi sáng diệu kì",
    #     "price": 110000,
    #     "image": "images/combo-buoi-sang-dieu-ky.jpg",
    #     "created_date": "2021-06-04",
    #     "quantity": 300,
    #     "category_id": 10,
    #     "author_id": 1
    # }, {
    #     "id": 8,
    #     "name": "Lược sử loài người",
    #     "description": "Lược sử loài người",
    #     "price": 1700000,
    #     "image": "images/combo-luoc-su-loai-nguoi.jpg",
    #     "created_date": "2021-06-04",
    #     "quantity": 600,
    #     "category_id": 6,
    #     "author_id": 3
    # }, {
    #     "id": 9,
    #     "name": "Mẹ con sư tử",
    #     "description": "Mẹ con sư tử",
    #     "price": 50000,
    #     "image": "images/combo-me-con-su-tu-bo-tat-ngan-tay-ngan-mat.jpg",
    #     "created_date": "2021-06-04",
    #     "quantity": 100,
    #     "category_id": 4,
    #     "author_id": 2
    # }, {
    #     "id": 10,
    #     "name": "Đường mây trên đất hoa",
    #     "description": "Đường mây trên đất hoa",
    #     "price": 130000,
    #     "image": "images/duong-may-tren-dat-hoa.jpg",
    #     "created_date": "2021-06-04",
    #     "quantity": 200,
    #     "category_id": 5,
    #     "author_id": 3
    # }]
    #
    # for p in products:
    #     pro = Product(name=p['name'], price=p['price'], image=p['image'], quantity=p['quantity'],
    #                   created_date=p['created_date'],
    #                   description=p['description'], category_id=p['category_id'], author_id=p['author_id'])
    #     db.session.add(pro)
    #
    # db.session.commit()
