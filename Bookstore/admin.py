from Bookstore import db, app, utils

from Bookstore.models import User, UserRole, Category, Product, ReceiptDetail
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request

from datetime import datetime


class AdminAutheticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class ProductView(AdminAutheticatedView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    can_create = True
    can_delete = True
    can_edit = True
    column_filters = ['name', 'price', 'id']
    column_labels = {
        'id': 'Mã sản phẩm',
        'name': 'Tên sản phẩm',
        'description': 'Mô tả',
        'price': 'Giá',
        'image': 'Ảnh sản phẩm',
        'quantity': 'Số lượng'
    }
    column_exclude_list = ['active', 'category', 'author', 'created_date']


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


class ReceiptView(BaseView):
    @expose("/")
    def index(self):
        re_details = ReceiptDetail.query.all()

        return self.render('admin/receipt.html', re_datails=re_details)


class InputView(BaseView):
    @expose("/", methods=['get', 'post'])
    def index(self):
        error_msg = ""
        if request.method.__eq__('POST'):
            try:
                name = request.form.get('name')
                quantity = request.form.get('quantity')

                try:
                    utils.update_book(name=name, quantity=quantity)
                except Exception as ex:
                    error_msg = str(ex)
            except Exception as ex:
                error_msg = str(ex)
        return self.render('admin/input_list.html')


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
admin.add_view(ReceiptView(name="Hóa đơn"))
admin.add_view(InputView(name="Nhập sách"))
# admin.add_view(AdminAutheticatedView(Regulation,db.session, name='Qui Định'))
admin.add_view(LogoutView(name="Đăng Xuất"))
