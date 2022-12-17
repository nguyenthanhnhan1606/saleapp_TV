from sqlalchemy import func
from saleapptv.models import TheLoaiSach, Sach, User, Receipt,ReceiptDetails,UserRole
from saleapptv import db
from flask_login import current_user
import hashlib


def load_TheLoaiSach():
    return TheLoaiSach.query.all()

def load_Sach(Ma_TL=None, kw=None):
    query = Sach.query

    if Ma_TL:
        query = query.filter(Sach.Sach_Tl.__eq__(Ma_TL))

    if kw:
        query = query.filter(Sach.TenSach.contains(kw))

    return query.all()

def get_sach_by_id(MaSach):
    return Sach.query.get(MaSach)

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(username, password,name, ngaysinh,diachi,email,sdt):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(username=username.strip(), password=password, Ten = name,NgaySinh = ngaysinh,DiaChi = diachi,Email =  email,DienThaoi = sdt)
    db.session.add(u)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)

def save_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['GiaTien'],
                               receipt=r, product_id=c['MaSach'])
            db.session.add(d)

        db.session.commit()

def count_product_by_cate():
    return db.session.query(TheLoaiSach.MaTLS, TheLoaiSach.TenTheLoai, func.count(Sach.MaSach))\
             .join(Sach, Sach.Sach_Tl.__eq__(TheLoaiSach.MaTLS), isouter=True)\
             .group_by(TheLoaiSach.MaTLS).all()


def total_amount():
    query = db.session.query(Sach.MaSach, Sach.TenSach, func.sum(ReceiptDetails.quantity*ReceiptDetails.price))\
                      .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Sach.MaSach))\
                      .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

    return query.all()


def total_quantity():
    query = db.session.query(Sach.MaSach, Sach.TenSach, func.sum(ReceiptDetails.quantity))\
                      .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Sach.MaSach))\
                      .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

    return query.all()


def total():
    m = []
    n = 0
    m = total_amount()
    for x in m:
        n = x[2]
    return n


def totalSL():
    m = []
    n = 0
    m = total_quantity()
    for x in m:
        n = x[2]
    return n



def stats_revenue(kw=None, from_date=None, to_date=None):
    query = db.session.query(TheLoaiSach.TenTheLoai, Sach.TenSach,func.sum(ReceiptDetails.quantity),func.sum(ReceiptDetails.quantity/totalSL()*100))\
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Sach.MaSach)) \
        .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id)) \
        .join(TheLoaiSach, Sach.Sach_Tl.__eq__((TheLoaiSach.MaTLS)))

    if kw:
        query = query.filter(Sach.TenSach.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query.group_by(Sach.MaSach).order_by(-Sach.MaSach).all()



def stats_revenueDT(kw=None, from_date=None, to_date=None):
    query = db.session.query(TheLoaiSach.TenTheLoai, Sach.MaSach,func.sum(ReceiptDetails.quantity*ReceiptDetails.price),func.sum(ReceiptDetails.quantity*ReceiptDetails.price)/total()*100)\
                      .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Sach.MaSach))\
                      .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))\
                      .join(TheLoaiSach, Sach.Sach_Tl.__eq__((TheLoaiSach.MaTLS)))

    if kw:
        query = query.filter(Sach.TenSach.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query.group_by(Sach.Sach_Tl).order_by(Sach.Sach_Tl).all()



if __name__ == '__main__':
    from saleapptv import app
    with app.app_context():
        print(stats_revenue())






