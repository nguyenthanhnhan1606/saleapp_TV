from flask import render_template, request, redirect, session, jsonify
from flask_login import login_user, logout_user, current_user
from saleapptv import app, dao, admin, login, utils
from saleapptv.decorators import annonymous_user
from saleapptv.models import UserRole


def index():
    Ma_TL = request.args.get('Ma_TL')
    kw = request.args.get('keyword')
    Sach = dao.load_Sach(Ma_TL=Ma_TL, kw=kw)
    TheLoaiSach = dao.load_TheLoaiSach()
    return render_template('index.html', Sach=Sach, TheLoaiSach=TheLoaiSach)


def details(MaSach):
    s = dao.get_sach_by_id(MaSach=MaSach)
    return render_template('details.html', Sach=s)


def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        name = request.form['name']
        ngaysinh = request.form['ngaysinh']
        diachi = request.form['diachi']
        email = request.form['email']
        sdt = request.form['sdt']
        if password.__eq__(confirm):
            try:
                dao.register(username=request.form['username'],
                             password=password, name=name, ngaysinh=ngaysinh, diachi=diachi, email=email, sdt=sdt)
                return redirect('/login')
            except Exception as e:
                err_msg = e
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@annonymous_user
def login_my_user():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            n = request.args.get('next')
            return redirect(n if n else '/')
        else:
            err_msg = "Đăng nhập không thành công. Tài khoản hoặc mật khẩu không đúng!!!"
    return render_template('login.html', err_msg=err_msg)


def admin_login():
    username = request.form['username']
    password = request.form['password']
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
        session['role'] = str(current_user.User_role)
    return redirect('/admin')


def load_user(user_id):
    return dao.get_user_by_id(user_id)


def logout_my_user():
    logout_user()
    return redirect('/login')


def cart():
    return render_template('cart.html')

def add_to_cart():
    data = request.json
    MaSach = str(data['MaSach'])

    key = app.config['CART_KEY_1']  # 'cart'
    cart = session[key] if key in session else {}
    if MaSach in cart:
        cart[MaSach]['quantity'] += 1
    else:
        TenSach = data['TenSach']
        GiaTien = data['GiaTien']

        cart[MaSach] = {
            "MaSach": MaSach,
            "TenSach": TenSach,
            "GiaTien": GiaTien,
            "quantity": 1
        }
    session[key] = cart
    return jsonify(utils.cart_stats(cart))


def update_cart(MaSach):
    key = app.config['CART_KEY_1']

    cart = session.get(key)
    if cart and MaSach in cart:
        cart[MaSach]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def delete_cart(MaSach):
    key = app.config['CART_KEY_1']
    cart = session.get(key)

    if cart and MaSach in cart:
        del cart[MaSach]

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def pay():
    key = app.config['CART_KEY_1']  # 'cart'
    cart = session.get(key)
    # import pdb
    # pdb.set_trace()
    try:
        dao.save_receipt(cart)
    except Exception as ex:
        print(str(ex))
        return jsonify({'status': 500})
    else:
        del session[key]

    return jsonify({'status': 200})


