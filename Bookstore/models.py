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
    avatar = Column(String(100), default='image/logo.png')
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    db.create_all()

    # users = [{
    #     "name": "Ad",
    #     "username": "admin123123",
    #     "password": "123123",
    #     "email": "admin@gmail.com",
    #     "avatar": "image/logo.jpg",
    #     "user_role": "ADMIN"
    # }, {
    #     "name": "Anh",
    #     "username": "AnhAnh",
    #     "password": "123123",
    #     "email": "anh@gmail.com",
    #     "avatar": "image/logo.jpg",
    #     "user_role": "USER"
    # }, {
    #     "name": "Bảo",
    #     "username": "Bao",
    #     "password": "123",
    #     "email": "bao@gmail.com",
    #     "avatar": "image/logo.jpg",
    #     "user_role": "USER"
    # }]
    #
    # for p in users:
    #     u = User(name=p['name'], username=p['username'], password=p['password'],
    #              email=p['email'], avatar=p['avatar'], user_role=p['user_role'])
    #     db.session.add(u)
    #
    # db.session.commit()
