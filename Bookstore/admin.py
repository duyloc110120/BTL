from Bookstore import db, app, utils

from Bookstore.models import User, UserRole, Category, Product
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request

from datetime import datetime


class AdminAutheticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class ProductView(AdminAutheticatedView):
    can_export = True
    column_filters = ['name', 'price']
    column_searchable_list = ['name']


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = utils.cate_stats()
        return self.render('admin/index.html', stats=stats)


class StatsView(BaseView):
    @expose("/")
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)

        return self.render('admin/stats.html',
                           month_stats=utils.product_month_stats(year=year),
                           stats=utils.product_stats(kw=kw,
                                                     from_date=from_date,
                                                     to_date=to_date))


class RegulationsView(AdminAutheticatedView):
    column_display_pk = True
    can_create = True
    can_delete = False
    can_edit = True
    can_export = True
    form_columns = ()


admin = Admin(app=app,
              name='Quản Trị BookStore Trực Tuyến',
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())

admin.add_view(AdminAutheticatedView(User, db.session))
admin.add_view(AdminAutheticatedView(Category, db.session, name="Danh mục"))
admin.add_view(ProductView(Product, db.session, name="Sản phẩm"))
admin.add_view(StatsView(name="Thống Kê Báo Cáo"))
# admin.add_view(AdminAutheticatedView(Regulation,db.session, name='Qui Định'))
admin.add_view(LogoutView(name="Đăng Xuất"))
