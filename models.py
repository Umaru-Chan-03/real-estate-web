from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ======================================================
# BANG BAT DONG SAN CHINH
# ======================================================

class BatDongSan(db.Model):
    __tablename__ = 'bat_dong_san'

    # ===== THONG TIN NHAN DIEN =====

    id = db.Column(db.Integer, primary_key=True)  
    # Khoa chinh tu dong tang

    ma_bat_dong_san = db.Column(db.String(50), unique=True, nullable=False)
    # Ma hien thi ngoai web (VD: BDS001)

    ma_noi_bo = db.Column(db.String(50))
    # Ma quan ly noi bo trong cong ty

    tieu_de = db.Column(db.String(255), nullable=False)
    # Tieu de hien thi tren web

    mo_ta_chi_tiet = db.Column(db.Text)
    # Noi dung mo ta chi tiet


    # ===== THONG TIN GIA =====

    # ===== THONG TIN GIA =====

    gia_vnd = db.Column(db.Float)
    gia_usd = db.Column(db.Float)
    gia_jpy = db.Column(db.Float)

    gia_moi_m2 = db.Column(db.Float)
    # Gia tren moi met vuong (co the tinh tu dong)

    co_thuong_luong = db.Column(db.Boolean, default=False)
    # True neu co the thuong luong


    # ===== THONG TIN VI TRI =====

    quoc_gia = db.Column(db.String(100), default='Việt Nam')
    # Quoc gia

    thanh_pho = db.Column(db.String(100))
    # Thanh pho

    quan_huyen = db.Column(db.String(100))
    # Quan / Huyen

    phuong_xa = db.Column(db.String(100))
    # Phuong / Xa

    ten_duong = db.Column(db.String(255))
    # Ten duong

    vi_do = db.Column(db.Float)
    # Latitude GPS vi_do = 21.028511

    kinh_do = db.Column(db.Float)
    # Longitude GPS kinh_do = 105.852020


    # ===== DIEN TICH VA CAU TRUC =====

    tong_dien_tich = db.Column(db.Float)
    # Tong dien tich (m2)

    so_phong_ngu = db.Column(db.Integer)
    # So phong ngu

    so_phong_tam = db.Column(db.Integer)
    # So phong tam

    so_tang = db.Column(db.Integer)
    # So tang


    # ===== PHAN LOAI =====

    loai_bat_dong_san = db.Column(db.String(50))
    # Phong / Nha / Can_ho / Dat

    loai_giao_dich = db.Column(db.String(50))
    # Ban / Cho_thue

    tinh_trang_phap_ly = db.Column(db.String(100))
    # So_do / Dang_cho_cap / ...

    hinh_thuc_so_huu = db.Column(db.String(100))
    # Lau_dai / 50_nam ...


    # ===== TRANG THAI HE THONG =====

    trang_thai = db.Column(db.String(50), default='Available')
    # Available / Sold / Rented

    tin_noi_bat = db.Column(db.Boolean, default=False)
    # True neu la tin noi bat

    luot_xem = db.Column(db.Integer, default=0)
    # Dem so luot xem

    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    # Thoi gian tao

    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Tu dong cap nhat khi sua


class BatDongSanTranslation(db.Model):

    __tablename__ = "bat_dong_san_translation"

    id = db.Column(db.Integer, primary_key=True)

    bat_dong_san_id = db.Column(
        db.Integer,
        db.ForeignKey("bat_dong_san.id"),
        nullable=False
    )

    language = db.Column(db.String(10), nullable=False)

    tieu_de = db.Column(db.String(255))
    mo_ta_chi_tiet = db.Column(db.Text)

    # ===== PHAN LOAI =====

    loai_bat_dong_san = db.Column(db.String(50))
    # Phong / Nha / Can_ho / Dat

    loai_giao_dich = db.Column(db.String(50))
    # Ban / Cho_thue

    tinh_trang_phap_ly = db.Column(db.String(100))
    # So_do / Dang_cho_cap / ...

    hinh_thuc_so_huu = db.Column(db.String(100))
    # Lau_dai / 50_nam ...


    bat_dong_san = db.relationship(
        "BatDongSan",
        backref=db.backref("translations", lazy=True)
    )

# ======================================================
# BANG HINH ANH BAT DONG SAN
# ======================================================

class HinhAnhBatDongSan(db.Model):
    __tablename__ = "hinh_anh_bat_dong_san"

    id = db.Column(db.Integer, primary_key=True)

    bat_dong_san_id = db.Column(
        db.Integer,
        db.ForeignKey("bat_dong_san.id"),
        nullable=False
    )

    # ĐỔI TÊN CHO ĐÚNG VỚI DB
    ten_hinh_anh = db.Column(db.String(255), nullable=False)

    bat_dong_san = db.relationship(
        "BatDongSan",
        backref=db.backref("danh_sach_hinh_anh", lazy=True)
    )


class QuocGia(db.Model):
    __tablename__ = "quoc_gia"

    id = db.Column(db.Integer, primary_key=True)
    ten_quoc_gia = db.Column(db.String(100), unique=True, nullable=False)

    thanh_pho_list = db.relationship(
        "ThanhPho",
        backref="quoc_gia",
        cascade="all, delete-orphan"
    )


class ThanhPho(db.Model):
    __tablename__ = "thanh_pho"

    id = db.Column(db.Integer, primary_key=True)

    ten_thanh_pho = db.Column(db.String(100), nullable=False)

    quoc_gia_id = db.Column(
        db.Integer,
        db.ForeignKey("quoc_gia.id"),
        nullable=False
    )

    # Thêm 2 cột mới
    vi_do = db.Column(db.Float)      # latitude
    kinh_do = db.Column(db.Float)    # longitude