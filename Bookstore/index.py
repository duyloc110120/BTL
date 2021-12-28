from Bookstore import app, loginn
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
import cloudinary.uploader
import utils
from Bookstore.admin import *


@app.route('/')
def home():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = utils.load_products(cate_id=cate_id, kw=kw)

    return render_template('index.html', products=products)


@app.route('/details')
def details():
    return render_template('product_details.html')


#
@app.route('/login', methods=['get', 'post'])
def login():
    #     error_msg = ""
    #     if request.method.__eq__('POST'):
    #         try:
    #             username = request.form['username']
    #             password = request.form['password']
    #
    #             user = utils.check_user(username=username, password=password)
    #             if user:
    #                 login_user(user=user)
    #
    #                 next = request.args.get('next', 'home')
    #                 return redirect(url_for(next))
    #             else:
    #                 error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"
    #
    #         except Exception as ex:
    #             error_msg = str(ex)
    #
    return render_template('login.html')


#
#
@app.route('/register', methods=['get', 'post'])
def register():
    #     err_msg = ''
    #     if request.method.__eq__('POST'):
    #         name = request.form.get('name')
    #         username = request.form.get('username')
    #         password = request.form.get('password')
    #         confirm = request.form.get('confirm')
    #         email = request.form.get('email')
    #
    #         if password.strip().__eq__(confirm.strip()):
    #             file = request.files.get('avatar')
    #             avatar = None
    #             if file:
    #                 res = cloudinary.uploader.upload(file)
    #                 avatar = res['secure_url']
    #
    #             try:
    #                 utils.create_user(name=name, password=password,
    #                                   username=username, email=email,
    #                                   avatar=avatar)
    #
    #                 return redirect(url_for('login'))
    #             except Exception as ex:
    #                 err_msg = 'Da co loi xay ra: ' + str(ex)
    #         else:
    #             err_msg = 'Mat khau KHONG khop!'
    #
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/admin-login", methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_user(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect('/admin')


@loginn.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)
