from flask import Flask
from config import Config
from models import db, BatDongSan, HinhAnhBatDongSan
import os
from models import QuocGia, ThanhPho
from models import BatDongSanTranslation
from werkzeug.utils import secure_filename
from datetime import datetime

# ==============================
# KHOI TAO APP & DB
# ==============================

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def xoa_toan_bo_bang():
    with app.app_context():
        db.drop_all()
        print("Da xoa toan bo bang")
# ==============================
# TAO BANG
# ==============================

def tao_bang():
    with app.app_context():
        db.create_all()
        print("Da tao bang (neu chua ton tai)")


# ==============================
# THEM BAT DONG SAN
# ==============================

def them_bat_dong_san(**kwargs):
    with app.app_context():

        if BatDongSan.query.filter_by(
            ma_bat_dong_san=kwargs.get("ma_bat_dong_san")
        ).first():
            print("Ma bat dong san da ton tai")
            return False

        bds = BatDongSan(**kwargs)

        db.session.add(bds)
        db.session.commit()

        print("Da them bat dong san")
        return True


# ==============================
# XOA BAT DONG SAN THEO MA
# ==============================

def xoa_bat_dong_san(ma_bds):
    with app.app_context():
        bds = BatDongSan.query.filter_by(
            ma_bat_dong_san=ma_bds
        ).first()

        if not bds:
            print("Khong tim thay bat dong san")
            return False

        db.session.delete(bds)
        db.session.commit()

        print("Da xoa bat dong san")
        return True


# ==============================
# CAP NHAT BAT DONG SAN
# ==============================

def cap_nhat_bat_dong_san(ma_bds, **kwargs):
    with app.app_context():
        bds = BatDongSan.query.filter_by(
            ma_bat_dong_san=ma_bds
        ).first()

        if not bds:
            print("Khong tim thay bat dong san")
            return False

        for key, value in kwargs.items():
            setattr(bds, key, value)

        db.session.commit()
        print("Da cap nhat bat dong san")
        return True


# ==============================
# LAY DANH SACH BAT DONG SAN
# ==============================

def lay_danh_sach():
    with app.app_context():
        return BatDongSan.query.all()


# ==============================
# TIM THEO MA
# ==============================

def tim_theo_ma(ma_bds):
    with app.app_context():
        return BatDongSan.query.filter_by(
            ma_bat_dong_san=ma_bds
        ).first()


# ==============================
# TANG LUOT XEM
# ==============================

def tang_luot_xem(ma_bds):
    with app.app_context():
        bds = BatDongSan.query.filter_by(
            ma_bat_dong_san=ma_bds
        ).first()

        if bds:
            bds.luot_xem += 1
            db.session.commit()
            print("Da tang luot xem")




def them_hinh_anh_cho_bds(ma_bds, danh_sach_ten_hinh):
    with app.app_context():

        bds = BatDongSan.query.filter_by(ma_bat_dong_san=ma_bds).first()

        if not bds:
            print("Không tìm thấy BĐS")
            return

        for ten in danh_sach_ten_hinh:
            hinh = HinhAnhBatDongSan(
                bat_dong_san_id=bds.id,
                ten_hinh_anh=ten
            )
            db.session.add(hinh)

        db.session.commit()
        print("Đã thêm ảnh cho BĐS:", ma_bds)

def xoa_1_hinh_anh(ma_bds, ten_hinh):
    with app.app_context():

        bds = BatDongSan.query.filter_by(ma_bat_dong_san=ma_bds).first()

        if not bds:
            print("Không tìm thấy BĐS")
            return

        hinh = HinhAnhBatDongSan.query.filter_by(
            bat_dong_san_id=bds.id,
            ten_hinh_anh=ten_hinh
        ).first()

        if not hinh:
            print("Không tìm thấy ảnh")
            return

        db.session.delete(hinh)
        db.session.commit()

        print("Đã xoá ảnh:", ten_hinh)

def xoa_toan_bo_hinh_anh(ma_bds):
    with app.app_context():

        bds = BatDongSan.query.filter_by(ma_bat_dong_san=ma_bds).first()

        if not bds:
            print("Không tìm thấy BĐS")
            return

        for hinh in bds.danh_sach_hinh_anh:
            db.session.delete(hinh)

        db.session.commit()

        print("Đã xoá toàn bộ ảnh của", ma_bds)

def hien_thi_hinh_anh(ma_bds):
    with app.app_context():

        bds = BatDongSan.query.filter_by(ma_bat_dong_san=ma_bds).first()

        if not bds:
            print("Không tìm thấy BĐS")
            return

        print("Danh sách ảnh của", ma_bds)

        for hinh in bds.danh_sach_hinh_anh:
            print(" -", hinh.ten_hinh_anh)













# ====================================================================================================================================================================================
# ====================================================================================================================================================================================
# ====================================================================================================================================================================================



def import_thanh_pho(file_path, ten_quoc_gia, country_code):
    # FILE_PATH = "data/cities5000.txt"
    # COUNTRY_CODE = "JP"
    # TEN_QUOC_GIA = "Japan"
    with app.app_context():

        # Kiểm tra quốc gia
        qg = QuocGia.query.filter_by(ten_quoc_gia=ten_quoc_gia).first()

        if not qg:
            qg = QuocGia(ten_quoc_gia=ten_quoc_gia)
            db.session.add(qg)
            db.session.commit()

        count = 0

        with open(file_path, encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")

                country_code = parts[8]

                if country_code == country_code:

                    ten_thanh_pho = parts[1]
                    latitude = parts[4]
                    longitude = parts[5]

                    tp = ThanhPho(
                        ten_thanh_pho=ten_thanh_pho,
                        quoc_gia_id=qg.id,
                        vi_do=float(latitude),
                        kinh_do=float(longitude)
                    )

                    db.session.add(tp)
                    count += 1

        db.session.commit()

        print("Da import", count, "thanh pho cho", ten_quoc_gia)

def tim_toa_do_thanh_pho(ten_thanh_pho):
    with app.app_context():

        tp = ThanhPho.query.filter(
            ThanhPho.ten_thanh_pho.ilike(ten_thanh_pho)
        ).first()

        if tp:
            print("Thanh pho:", tp.ten_thanh_pho)
            print("Vi do:", tp.vi_do)
            print("Kinh do:", tp.kinh_do)
        else:
            print("Khong tim thay thanh pho")
def lay_danh_sach_thanh_pho_viet_nam():
    with app.app_context():

        qg = QuocGia.query.filter_by(ten_quoc_gia="Viet Nam").first()

        if not qg:
            print("Khong tim thay quoc gia")
            return []

        ds_thanh_pho = ThanhPho.query.filter_by(
            quoc_gia_id=qg.id
        ).all()

        # Lưu vào biến Python
        danh_sach = [
            {
                "ten": tp.ten_thanh_pho,
                "vi_do": tp.vi_do,
                "kinh_do": tp.kinh_do
            }
            for tp in ds_thanh_pho
        ]

        return danh_sach


def tim_kiem_bat_dong_san(
    loai_giao_dich=None,
    loai_bds=None,
    ten_quoc_gia=None,
    ten_thanh_pho=None,
    gia_min=None,
    gia_max=None,
    don_vi_tien="VND",
    dien_tich_min=None,
    dien_tich_max=None,
    phong_ngu_min=None,
    phong_ngu_max=None
):
    with app.app_context():

        query = BatDongSan.query

        # 🔹 Lọc loại giao dịch
        if loai_giao_dich:
            query = query.filter(BatDongSan.loai_giao_dich == loai_giao_dich)

        # 🔹 Lọc loại BĐS
        if loai_bds:
            query = query.filter(BatDongSan.loai_bat_dong_san == loai_bds)

        # 🔹 Lọc vị trí
        if ten_thanh_pho:
            query = query.filter(
                BatDongSan.thanh_pho == ten_thanh_pho
            )

        elif ten_quoc_gia:
            query = query.filter(
                BatDongSan.quoc_gia == ten_quoc_gia
            )

        # 🔹 Lọc giá (convert về VND)
        # 🔹 Lọc giá theo đơn vị được chọn
        if gia_min is not None and gia_max is not None:
            if don_vi_tien == "VND":
                query = query.filter(
                    BatDongSan.gia_vnd >= gia_min,
                    BatDongSan.gia_vnd <= gia_max
                )

            elif don_vi_tien == "USD":
                query = query.filter(
                    BatDongSan.gia_usd >= gia_min,
                    BatDongSan.gia_usd <= gia_max
                )

            elif don_vi_tien == "JPY":
                query = query.filter(
                    BatDongSan.gia_jpy >= gia_min,
                    BatDongSan.gia_jpy <= gia_max
                )

        # 🔹 Lọc diện tích
        if dien_tich_min is not None:
            query = query.filter(BatDongSan.tong_dien_tich >= dien_tich_min)

        if dien_tich_max is not None:
            query = query.filter(BatDongSan.tong_dien_tich <= dien_tich_max)

        # 🔹 Lọc phòng ngủ
        if phong_ngu_min is not None:
            query = query.filter(BatDongSan.so_phong_ngu >= phong_ngu_min)

        if phong_ngu_max is not None:
            query = query.filter(BatDongSan.so_phong_ngu <= phong_ngu_max)

        ket_qua = query.all()

        print("Tim thay", len(ket_qua), "bat dong san")

        for bds in ket_qua:
            print(bds.ma_bat_dong_san, bds.tieu_de, bds.gia_vnd)

        return ket_qua
    



def hien_thi_tien(gia, ma_tien):
    if ma_tien == "VND":
        return f"{gia:,.0f} ₫"
    elif ma_tien == "USD":
        return f"${gia:,.0f}"
    elif ma_tien == "JPY":
        return f"¥{gia:,.0f}"





def them_ban_dich(
    ma_bds,
    language,
    tieu_de=None,
    mo_ta_chi_tiet=None,
    loai_bat_dong_san=None,
    loai_giao_dich=None,
    tinh_trang_phap_ly=None,
    hinh_thuc_so_huu=None
):

    with app.app_context():

        bds = BatDongSan.query.filter_by(
            ma_bat_dong_san=ma_bds
        ).first()

        if not bds:
            print("Không tìm thấy BĐS")
            return

        trans = BatDongSanTranslation(
            bat_dong_san_id=bds.id,
            language=language,
            tieu_de=tieu_de,
            mo_ta_chi_tiet=mo_ta_chi_tiet,
            loai_bat_dong_san=loai_bat_dong_san,
            loai_giao_dich=loai_giao_dich,
            tinh_trang_phap_ly=tinh_trang_phap_ly,
            hinh_thuc_so_huu=hinh_thuc_so_huu
        )

        db.session.add(trans)
        db.session.commit()

        print("Đã thêm bản dịch", language)

def lay_bds_theo_ngon_ngu(language="VI"):
    with app.app_context():

        ds = BatDongSan.query.all()

        result = []

        for bds in ds:

            data = {
                "ma_bds": bds.ma_bat_dong_san,
                "tieu_de": bds.tieu_de,
                "mo_ta_chi_tiet": bds.mo_ta_chi_tiet,
                "loai_bds": bds.loai_bat_dong_san,
                "loai_giao_dich": bds.loai_giao_dich,
                "gia_vnd": bds.gia_vnd,
                "thanh_pho": bds.thanh_pho,
                "quan_huyen": bds.quan_huyen,
                "so_phong_ngu": bds.so_phong_ngu,
                "tong_dien_tich": bds.tong_dien_tich
            }

            # tìm bản dịch
            trans = BatDongSanTranslation.query.filter_by(
                bat_dong_san_id=bds.id,
                language=language
            ).first()

            if trans:
                if trans.tieu_de:
                    data["tieu_de"] = trans.tieu_de

                if trans.mo_ta_chi_tiet:
                    data["mo_ta_chi_tiet"] = trans.mo_ta_chi_tiet

                if trans.loai_bat_dong_san:
                    data["loai_bds"] = trans.loai_bat_dong_san

                if trans.loai_giao_dich:
                    data["loai_giao_dich"] = trans.loai_giao_dich

            result.append(data)

        return result
        

# Thêm vào cuối file database_manager.py hoặc khu vực các hàm lấy dữ liệu

def get_all_properties():
    with app.app_context():
        # Lấy tất cả bản ghi từ bảng BatDongSan
        items = BatDongSan.query.order_by(BatDongSan.id.desc()).all()
        
        result = []
        for item in items:
            # Chuyển đổi object thành dictionary để dễ hiển thị ở frontend
            result.append({
                "id": item.id,
                "ma_bds": item.ma_bat_dong_san,
                "tieu_de": item.tieu_de,
                "gia": item.gia_vnd,
                "vi_do": item.vi_do,
                "kinh_do": item.kinh_do,
                "dien_tich": item.tong_dien_tich,
                "loai_bds": item.loai_bat_dong_san,
                "ma_tp": item.thanh_pho,
                "anh": item.anh_dai_dien if hasattr(item, 'anh_dai_dien') else ""
            })
        return result

def save_property_to_db(data, files=None, IMAGE_FOLDER="data/images"):
    with app.app_context():
        try:
            ma_bds = data.get('ma_bat_dong_san')
            # Tìm xem đã có mã này chưa để Update, nếu chưa thì tạo mới
            bds = BatDongSan.query.filter_by(ma_bat_dong_san=data.get('ma_bat_dong_san')).first()
            if not bds:
                # bds = BatDongSan(ma_bat_dong_san=data.get('ma_bat_dong_san'))
                # db.session.add(bds)
                them_bat_dong_san(
                                    ma_bat_dong_san=ma_bds,
                                    ma_noi_bo=ma_bds,
                                    tieu_de=data.get('tieu_de'),
                                    mo_ta_chi_tiet=data.get('mo_ta_chi_tiet'),
                                    gia_vnd=data.get('gia_vnd'),
                                    gia_usd=data.get('gia_usd'),
                                    gia_jpy=data.get('gia_jpy', None),  # <-- Đây là cột bạn muốn để trống
                                    gia_moi_m2 = data.get('gia_moi_m2'),
                                    quoc_gia=data.get('quoc_gia'),
                                    thanh_pho=data.get('thanh_pho'),
                                    quan_huyen=data.get('quan_huyen'),
                                    phuong_xa=data.get('phuong_xa'),
                                    ten_duong=data.get('ten_duong'),
                                    vi_do=data.get('vi_do'),
                                    kinh_do=data.get('kinh_do'),
                                    loai_bat_dong_san=data.get('loai_bat_dong_san'),
                                    loai_giao_dich=data.get('loai_giao_dich'),
                                    trang_thai=data.get('trang_thai', 'Available'),
                                    co_thuong_luong=data.get('co_thuong_luong', False),
                                    tin_noi_bat=data.get('tin_noi_bat', False),
                                    tong_dien_tich = data.get('tong_dien_tich'),
                                    so_phong_ngu = data.get('so_phong_ngu'),
                                    so_phong_tam=data.get('so_phong_tam'),
                                    so_tang = data.get('so_tang'),
                                    tinh_trang_phap_ly=data.get('tinh_trang_phap_ly'),
                                    hinh_thuc_so_huu=data.get('hinh_thuc_so_huu'),
                                    luot_xem=0,
                                    ngay_tao=datetime.now(),
                                    ngay_cap_nhat=datetime.now()
                                )
            else:
                # Gán giá trị (Dựa trên đúng tên cột trong models.py)
                # cap_nhat_bat_dong_san("BDS100", gia=5000000000)
                if data.get('tieu_de'):
                    cap_nhat_bat_dong_san(ma_bds, tieu_de=data.get('tieu_de'))
                if data.get('mo_ta_chi_tiet'):
                    cap_nhat_bat_dong_san(ma_bds, mo_ta_chi_tiet=data.get('mo_ta_chi_tiet'))
                if data.get('gia_vnd'):
                    cap_nhat_bat_dong_san(ma_bds, gia_vnd=data.get('gia_vnd'))
                if data.get('gia_usd'):
                    cap_nhat_bat_dong_san(ma_bds, gia_usd=data.get('gia_usd'))
                if data.get('gia_jpy'):
                    cap_nhat_bat_dong_san(ma_bds, gia_jpy=data.get('gia_jpy'))
                if data.get('gia_moi_m2'):
                    cap_nhat_bat_dong_san(ma_bds, gia_moi_m2=data.get('gia_moi_m2'))
                if data.get('co_thuong_luong'):
                    cap_nhat_bat_dong_san(ma_bds, co_thuong_luong=data.get('co_thuong_luong'))
                if data.get('tin_noi_bat'):
                    cap_nhat_bat_dong_san(ma_bds, tin_noi_bat=data.get('tin_noi_bat'))
                if data.get('quoc_gia'):
                    cap_nhat_bat_dong_san(ma_bds, quoc_gia=data.get('quoc_gia'))
                if data.get('thanh_pho'):
                    cap_nhat_bat_dong_san(ma_bds, thanh_pho=data.get('thanh_pho'))
                if data.get('quan_huyen'):
                    cap_nhat_bat_dong_san(ma_bds, quan_huyen=data.get('quan_huyen'))
                if data.get('phuong_xa'):
                    cap_nhat_bat_dong_san(ma_bds, phuong_xa=data.get('phuong_xa'))
                if data.get('ten_duong'):
                    cap_nhat_bat_dong_san(ma_bds, ten_duong=data.get('ten_duong'))
                if data.get('vi_do'):
                    cap_nhat_bat_dong_san(ma_bds, vi_do=data.get('vi_do'))
                if data.get('kinh_do'):
                    cap_nhat_bat_dong_san(ma_bds, kinh_do=data.get('kinh_do'))
                if data.get('tong_dien_tich'):
                    cap_nhat_bat_dong_san(ma_bds, tong_dien_tich=data.get('tong_dien_tich'))
                if data.get('so_phong_ngu'):
                    cap_nhat_bat_dong_san(ma_bds, so_phong_ngu=data.get('so_phong_ngu'))
                if data.get('so_phong_tam'):
                    cap_nhat_bat_dong_san(ma_bds, so_phong_tam=data.get('so_phong_tam'))
                if data.get('so_tang'):
                    cap_nhat_bat_dong_san(ma_bds, so_tang=data.get('so_tang'))
                if data.get('loai_bat_dong_san'):
                    cap_nhat_bat_dong_san(ma_bds, loai_bat_dong_san=data.get('loai_bat_dong_san'))
                if data.get('loai_giao_dich'):
                    cap_nhat_bat_dong_san(ma_bds, loai_giao_dich=data.get('loai_giao_dich'))
                if data.get('trang_thai'):
                    cap_nhat_bat_dong_san(ma_bds, trang_thai=data.get('trang_thai'))
                if data.get('tinh_trang_phap_ly'):
                    cap_nhat_bat_dong_san(ma_bds, tinh_trang_phap_ly=data.get('tinh_trang_phap_ly'))
                if data.get('hinh_thuc_so_huu'):
                    cap_nhat_bat_dong_san(ma_bds, hinh_thuc_so_huu=data.get('hinh_thuc_so_huu'))
            

            # Xử lý lưu ảnh
            if files:
                # Tạo thư mục cho BĐS này nếu chưa có
                target_dir = os.path.join(IMAGE_FOLDER, ma_bds)
                os.makedirs(target_dir, exist_ok=True)

                for file in files:
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(target_dir, filename))
                        
                        # Lưu vào bảng HinhAnhBatDongSan
                        new_img = HinhAnhBatDongSan(
                            bat_dong_san_id=bds.id,
                            ten_hinh_anh=filename
                        )
                        db.session.add(new_img)

            db.session.commit()
            return True
        except Exception as e:
            print(f"Lỗi: {e}")
            db.session.rollback()
            return False
def delete_property_by_id(ma_bds):
    with app.app_context():
        try:
            bds = BatDongSan.query.filter_by(ma_bat_dong_san=ma_bds).first()
            if bds:
                db.session.delete(bds)
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Lỗi khi xóa: {e}")
            db.session.rollback()
            return False
if __name__ == "__main__":

    DANH_SACH_QUOC_GIA = [
        {"code": "VN", "ten": "Viet Nam"},
        {"code": "JP", "ten": "Nhat Ban"},
        {"code": "KR", "ten": "Han Quoc"}
        ]
    FILE_PATH = "data/cities5000.txt"
    # COUNTRY_CODE = "VN"
    # TEN_QUOC_GIA = "Viet Nam"
    COUNTRY_CODE = "JP"
    TEN_QUOC_GIA = "Japan"
    
    # def test_toa_do():
    #     with app.app_context():
    #         tp = ThanhPho.query.first()
    #         print(tp.ten_thanh_pho, tp.vi_do, tp.kinh_do)
    # import_thanh_pho()
    # test_toa_do()

    # tim_toa_do_thanh_pho("Hưng Yên")
    # print(lay_danh_sach_thanh_pho_viet_nam())
    tim_kiem_bat_dong_san(ten_quoc_gia = "Viet Nam")