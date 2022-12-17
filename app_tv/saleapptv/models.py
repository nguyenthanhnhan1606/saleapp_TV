from sqlalchemy import  Column, Integer, String, Text, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from saleapptv import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

class User(BaseModel, UserMixin):
    username = Column(String(50), nullable=True)
    password = Column(String(50), nullable=True)
    User_role= Column(Enum(UserRole), default=UserRole.USER)
    Ten = Column(String(50), nullable=False)
    NgaySinh = Column(DateTime)
    DiaChi = Column(String(100))
    Email = Column(String(50))
    DienThaoi = Column(String(20))
    user_HD = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name



class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)

    def __str__(self):
        return self.name


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey('Sach.MaSach'), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)





class Sach(db.Model):
    __tablename__ = 'Sach'
    MaSach = Column(Integer,primary_key=True, autoincrement=True)
    TenSach = Column(String(50))
    TenTacGia = Column(String(100))
    GiaTien = Column(Float)
    img = Column(String(200))
    Sach_Tl =Column(Integer, ForeignKey('TheLoaiSach.MaTLS'),nullable=False)
    chitiethoadon=relationship('ReceiptDetails',backref='sach',lazy=True)

    def __str__(self):
        return self.TenSach


class TheLoaiSach(db.Model):
    __tablename__='TheLoaiSach'
    MaTLS = Column(Integer,primary_key=True, autoincrement=True)
    TenTheLoai = Column(String(100))
    sach = relationship(Sach, backref='TheLoaiSach', lazy=True)

    def __str__(self):
        return self.TenTheLoai


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # t1 = TheLoaiSach(TenTheLoai='Java')
        # t2 = TheLoaiSach(TenTheLoai='C/C++')
        # t3 = TheLoaiSach(TenTheLoai='Python')
        # t4 = TheLoaiSach(TenTheLoai='Javascript')
        # db.session.add_all([t1, t2, t3, t4])
        # db.session.commit()
        #
        # s1 = Sach(TenSach='Lập trình JAVA', TenTacGia='NTN', GiaTien=115000,
        #              img='https://sangtaotrongtamtay.vn/wp-content/uploads/2021/12/sach-lap-trinh-1.jpg', Sach_Tl=1)
        # s2 = Sach(TenSach='Lập Trình C/C++', TenTacGia='NTN', GiaTien=135000,
        #           img='https://sangtaotrongtamtay.vn/wp-content/uploads/2021/12/sach-lap-trinh-1.jpg', Sach_Tl=2)
        # s3 = Sach(TenSach='Lập trình Python', TenTacGia='NTN', GiaTien=200000,
        #         img='https://sangtaotrongtamtay.vn/wp-content/uploads/2021/12/sach-lap-trinh-1.jpg', Sach_Tl=3)
        # s4 = Sach(TenSach='Lập Trình C/C++ 2', TenTacGia='NTN', GiaTien=135000,
        #           img='https://sangtaotrongtamtay.vn/wp-content/uploads/2021/12/sach-lap-trinh-1.jpg', Sach_Tl=2)
        # s5 = Sach(TenSach='Lập Trình Javascript', TenTacGia='NTN', GiaTien=180000,
        #           img='https://sangtaotrongtamtay.vn/wp-content/uploads/2021/12/sach-lap-trinh-1.jpg', Sach_Tl=4)
        # s6 = Sach(TenSach='Lập trình Python 2', TenTacGia='NTN', GiaTien=140000,
        #           img='https://sangtaotrongtamtay.vn/wp-content/uploads/2021/12/sach-lap-trinh-1.jpg', Sach_Tl=3)
        # s7 = Sach(TenSach='Lập Trình JAVA 2', TenTacGia='NTN', GiaTien=125000,
        #           img='https://sangtaotrongtamtay.vn/wp-content/uploads/2021/12/sach-lap-trinh-1.jpg', Sach_Tl=1)
        # s8 = Sach(TenSach='Lập Trình Javascript 2', TenTacGia='NTN', GiaTien=160000,
        #           img='https://sangtaotrongtamtay.vn/wp-content/uploads/2021/12/sach-lap-trinh-1.jpg', Sach_Tl=4)
        #
        #
        # db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8])
        # db.session.commit()