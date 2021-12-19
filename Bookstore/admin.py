from Bookstore import db, app, utils

from Bookstore.models import User, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request

from datetime import datetime


class AdminAutheticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


admin = Admin(app=app,
              name='Quản Trị BookStore Trực Tuyến',
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())

admin.add_view(AdminAutheticatedView(User, db.session))
admin.add_view(LogoutView(name="Đăng Xuất"))
