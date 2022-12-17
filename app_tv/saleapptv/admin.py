from saleapptv.models import Sach, UserRole,TheLoaiSach
from saleapptv import db, app, dao
from flask_admin import Admin, BaseView, expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask import redirect,request

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class SachView(ModelView):
    column_searchable_list = ['TenSach', 'TenTacGia']
    column_filters = ['TenSach', 'GiaTien', 'TheLoaiSach']
    can_view_details = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
        'TenSach': 'Tên sách',
        'TenTacGia': 'Tên tác giả',
        'GiaTien': 'Giá',
        'TheLoaiSach': 'Tên thể loại'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaWidget
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.User_role==UserRole.ADMIN


class SachTLView(ModelView):
    column_searchable_list = ['TenTheLoai']
    column_filters = ['MaTLS', 'TenTheLoai']
    can_view_details = True
    can_export = True
    column_labels = {
        'TenTheLoai': 'Tên thể loại',
           'MaTLS':'Mã thể loại sách'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaWidget
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.User_role==UserRole.ADMIN


class BCDTView(ModelView):
    column_searchable_list = ['TheLoaiSach', 'DoanhThu']
    column_filters = ['TheLoaiSach', 'DoanhThu','SoLuotThue' ,'TyLe']
    can_view_details = True
    can_export = True
    column_labels = {
        'TheLoaiSach': 'Thể loại sách',
        'DoanhThu': 'Doanh thu',
        'SoLuotThue': 'Số lượt thuê',
        'TyLe': 'Tỷ lệ'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaWidget
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.User_role==UserRole.ADMIN



class BCTSView(ModelView):
    column_searchable_list = ['TenSach', 'TheLoaiSach']
    column_filters = ['TenSach', 'TheLoaiSach','SoLuong','TyLe']
    can_view_details = True
    can_export = True
    column_labels = {
        'TenSach': 'Tên sách',
        'TheLoaiSach': 'Thể loại sách',
        'SoLuong': 'Số Lượng',
        'TyLe': 'Tỷ lệ'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaWidget
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.User_role == UserRole.ADMIN


class LogoutView(BaseView):
   @expose('/')
   def index(self):
        logout_user()
        return redirect('/admin')

   def is_accessible(self):
       return current_user.is_authenticated




class StatsView(BaseView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenueDT(kw=request.args.get('kw'),
                                  from_date=request.args.get('from_date'),
                                  to_date=request.args.get('to_date'))
        return self.render('admin/stats.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.User_role == UserRole.ADMIN


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_product_by_cate()
        return self.render('admin/index.html', stats=stats)


class StatsViewTS(BaseView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue(kw=request.args.get('kw'),
                                  from_date=request.args.get('from_date'),
                                  to_date=request.args.get('to_date'))
        return self.render('admin/fqstats.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.User_role == UserRole.ADMIN


admin = Admin(app=app, name='Quản trị thư viện', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(SachView(Sach, db.session, name='Sách'))
admin.add_view(SachTLView(TheLoaiSach, db.session,name='Thể Loại Sách'))
admin.add_view(StatsView(name='Báo cáo doanh thu'))
admin.add_view(StatsViewTS(name='Báo cáo tần suất'))
admin.add_view(LogoutView(name='Đăng xuất'))

