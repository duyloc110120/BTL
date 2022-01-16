from Bookstore import app, loginn, decorator
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required
import cloudinary.uploader
import utils
from Bookstore.admin import *
from Bookstore.models import Product, Receipt, ReceiptDetail


@app.route('/')


def home():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = utils.load_products(cate_id=cate_id, kw=kw)

    return render_template('index.html', products=products)


@app.route('/products')
def product():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = utils.load_products(cate_id=cate_id, kw=kw)

    return render_template('product.html', products=products)


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    products = utils.get_product_by_id(product_id)

    return render_template('product_details.html', products=products)


@app.route('/login', methods=['get', 'post'])
def login():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            username = request.form['username']
            password = request.form['password']

            user = utils.check_user(username=username, password=password, role=UserRole.USER)
            if user:
                login_user(user=user)

                if 'next' in request.args:
                    return redirect(request.args['next'])

                return redirect(url_for('home'))
            else:
                error_msg = "Chương trình đang có lỗi !! Vui lòng thử lại sau"

        except Exception as ex:
            error_msg = str(ex)

    return render_template('login.html', error_msg=error_msg)


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')

        if password.strip().__eq__(confirm.strip()):
            file = request.files.get('avatar')
            avatar = None
            if file:
                res = cloudinary.uploader.upload(file)
                avatar = res['secure_url']

            try:
                utils.create_user(name=name, password=password,
                                  username=username, email=email,
                                  avatar=avatar)

                return redirect(url_for('login'))
            except Exception as ex:
                err_msg = 'Đã có lỗi xảy ra: ' + str(ex)
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/logout')
@decorator.login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/cart')
@decorator.login_required
def cart():
    return render_template('cart.html', cart_stats=utils.cart_stats(session.get('cart')))


@app.route("/admin/login", methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_user(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/api/add-to-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    cart = session.get('cart')
    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1

    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/api/update-cart', methods=['put'])
def update_cart():
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    cart = session.get('cart')
    if cart:
        if id in cart and quantity:
            cart[id]['quantity'] = quantity
            session['cart'] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart:
        if product_id in cart:
            del cart[product_id]
            session['cart'] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/api/pay', methods=['post'])
def pay():
    try:
        utils.add_receipt(session.get('cart'))

        del session['cart']
        return jsonify({'code': 200})
    except Exception as ex:
        print(str(ex))
        return jsonify({'code': 400})


@app.route('/bill')
def bill():
    return render_template('bill.html')


@loginn.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.context_processor
def common_response():
    return {
        'categories': utils.load_categories(),
        'cart_stats': utils.cart_stats(session.get('cart'))
    }


if __name__ == '__main__':
    app.run(debug=True)
