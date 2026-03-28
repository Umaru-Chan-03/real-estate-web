from flask import Flask, render_template, request, redirect
from config import Config
import os
from flask import send_from_directory
from models import db, BatDongSan, HinhAnhBatDongSan, BatDongSanTranslation # Import trực tiếp từ models
from models import ThanhPho, QuocGia
from flask import jsonify
from database_manager import lay_bds_theo_ngon_ngu
# Sửa lại phần import ở đầu file main.py (nếu chưa có)
import database_manager as db_mgr
import json


# Cấu hình đường dẫn ảnh
IMAGE_FOLDER = "./data/images"

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app) # Liên kết db với app chính ở đây

UI = {
    "website_title": "Trang BDS",

    "logo_text": "REAL ESTATE PRO",
    "logo_image": "images/logo.png",

    "menu_items": [
        {"name": "Trang chủ", "link": "/"},
        {"name": "Bán", "link": "/ban"},
        {"name": "Cho thuê", "link": "/thue"}
    ],

    "admin_login_text": "Admin",

    "languages": ["VI", "EN", "JP"]
}



# Đơn vị: Đồng (VNĐ)
gia_ban_vnd = {
    "don_vi": "₫",
    "min": [0, 1000000000, 2000000000, 3000000000, 5000000000, 7000000000, 10000000000, 15000000000, 20000000000],
    "max": [1000000000, 2000000000, 3000000000, 5000000000, 7000000000, 10000000000, 15000000000, 20000000000, 50000000000]
}

gia_thue_vnd = {
    "don_vi": "₫",
    "min": [0, 1000000, 2000000, 3000000, 5000000, 7000000, 10000000, 15000000],
    "max": [1000000, 2000000, 3000000, 5000000, 7000000, 10000000, 15000000, 20000000]
}

# Đơn vị: USD ($) - Giữ nguyên vì bạn đã để số đầy đủ
gia_ban_usd = {
    "don_vi": "$",
    "min": [0, 50000, 100000, 200000, 300000, 500000, 1000000],
    "max": [50000, 100000, 200000, 300000, 500000, 1000000, 5000000]
}

gia_thue_usd = {
    "don_vi": "$",
    "min": [0, 200, 500, 1000, 2000, 3000, 5000],
    "max": [200, 500, 1000, 2000, 3000, 5000, 10000]
}

# Đơn vị: Yên (¥) - Đã quy đổi từ Vạn (x10.000) và Nghìn (x1.000)
gia_ban_jpy = {
    "don_vi": "¥",
    "min": [0, 10000000, 20000000, 30000000, 50000000, 70000000, 100000000, 150000000, 200000000],
    "max": [10000000, 20000000, 30000000, 50000000, 70000000, 100000000, 150000000, 200000000, 500000000]
}

gia_thue_jpy = {
    "don_vi": "¥",
    "min": [0, 50000, 80000, 100000, 150000, 200000, 300000],
    "max": [50000, 80000, 100000, 150000, 200000, 300000, 500000]
}


FILTER_OPTIONS = {
    "tien_te": {
        "VND": {
            "ban": gia_ban_vnd,
            "thue": gia_thue_vnd
        },
        "USD": {
            "ban": gia_ban_usd,
            "thue": gia_thue_usd
        },
        "JPY": {
            "ban": gia_ban_jpy,
            "thue": gia_thue_jpy
        }
    }
}
@app.route("/")
def home():

    # ngôn ngữ
    lang = request.args.get("lang", "VI")

    # pagination
    page = request.args.get("page", 1, type=int)

    selected_filters = {
        "loai_giao_dich": request.args.get("loai_giao_dich", ""),
        "loai_bds": request.args.get("loai_bds", ""),
        "ten_quoc_gia": request.args.get("ten_quoc_gia", ""),
        "ten_thanh_pho": request.args.get("ten_thanh_pho", ""),
        "don_vi_tien": request.args.get("don_vi_tien", ""),
        "gia_min": request.args.get("gia_min", type=int),
        "gia_max": request.args.get("gia_max", type=int),
        "dien_tich_min": request.args.get("dien_tich_min", type=float),
        "dien_tich_max": request.args.get("dien_tich_max", type=float),
    }

    # Map giá trị từ URL sang giá trị trong DB

    loai_map = {
        "ban": "Bán",
        "thue": "Cho thuê"
    }

    country_map = {
        "VN": "Việt Nam",
        "JP": "Nhật Bản"
    }

    if selected_filters["loai_giao_dich"] in loai_map:
        selected_filters["loai_giao_dich"] = loai_map[selected_filters["loai_giao_dich"]]

    if selected_filters["ten_quoc_gia"] in country_map:
        selected_filters["ten_quoc_gia"] = country_map[selected_filters["ten_quoc_gia"]]

    query = BatDongSan.query

    # lọc loại giao dịch
    if selected_filters["loai_giao_dich"]:
        query = query.filter(
            BatDongSan.loai_giao_dich == selected_filters["loai_giao_dich"]
        )

    # lọc loại bds
    if selected_filters["loai_bds"]:
        query = query.filter(
            BatDongSan.loai_bat_dong_san == selected_filters["loai_bds"]
        )

    # lọc quốc gia
    if selected_filters["ten_quoc_gia"]:
        query = query.filter(
            BatDongSan.quoc_gia == selected_filters["ten_quoc_gia"]
        )

    # lọc thành phố
    if selected_filters["ten_thanh_pho"]:
        query = query.filter(
            BatDongSan.thanh_pho == selected_filters["ten_thanh_pho"]
        )

    # lọc giá
    if selected_filters["gia_min"] is not None:
        query = query.filter(
            BatDongSan.gia_vnd >= selected_filters["gia_min"]
        )

    if selected_filters["gia_max"] is not None:
        query = query.filter(
            BatDongSan.gia_vnd <= selected_filters["gia_max"]
        )

    # lọc diện tích
    if selected_filters["dien_tich_min"]:
        query = query.filter(
            BatDongSan.tong_dien_tich >= selected_filters["dien_tich_min"]
        )

    if selected_filters["dien_tich_max"]:
        query = query.filter(
            BatDongSan.tong_dien_tich <= selected_filters["dien_tich_max"]
        )

    # pagination
    pagination = query.order_by(
        BatDongSan.ngay_tao.desc()
    ).paginate(page=page, per_page=20)

    all_bds = pagination.items

    # =========================
    # ÁP DỤNG TRANSLATION
    # =========================

    if lang != "VI":

        for bds in all_bds:

            trans = BatDongSanTranslation.query.filter_by(
                bat_dong_san_id=bds.id,
                language=lang
            ).first()

            if trans:

                if trans.tieu_de:
                    bds.tieu_de = trans.tieu_de

                if trans.mo_ta_chi_tiet:
                    bds.mo_ta_chi_tiet = trans.mo_ta_chi_tiet

                if trans.loai_bat_dong_san:
                    bds.loai_bat_dong_san = trans.loai_bat_dong_san

                if trans.loai_giao_dich:
                    bds.loai_giao_dich = trans.loai_giao_dich

    # =========================
    # DATA CHO MAP
    # =========================




    # Chuẩn bị dữ liệu danh sách để gửi sang Javascript
    bds_list_json = []
    for item in pagination.items:
        bds_list_json.append({
            "ma_bds": item.ma_bat_dong_san,
            "tieu_de": item.tieu_de,
            "gia": f"{item.gia_vnd:,.0f} ₫",
            "vi_do": item.vi_do,
            "kinh_do": item.kinh_do,
            "anh": item.danh_sach_hinh_anh[0].ten_hinh_anh if item.danh_sach_hinh_anh else 'default.jpg'
        })

    return render_template(
        "index.html",
        ui=UI,
        filter_data=FILTER_OPTIONS,
        selected_filters=selected_filters,
        all_bds=all_bds,
        pagination=pagination,
        bds_json=bds_list_json # Gửi dữ liệu JSON này sang HTML
    )

# Sửa lại đoạn cấu hình đường dẫn trong main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Nếu thư mục data nằm cùng cấp với main.py, hãy dùng:
# IMAGE_FOLDER = os.path.join(BASE_DIR, "data", "images")

# Hoặc giữ nguyên đường dẫn tuyệt đối nhưng đảm bảo nó đúng:

@app.route('/property_images/<path:filename>')
def custom_static(filename):
    # Thêm log để kiểm tra sự tồn tại ngay trong code
    full_path = os.path.join(IMAGE_FOLDER, filename)
    if not os.path.exists(full_path):
        print(f"❌ KHÔNG TÌM THẤY: {full_path}")
    else:
        print(f"✅ ĐÃ THẤY FILE: {full_path}")
        
    return send_from_directory(IMAGE_FOLDER, filename)

# Thêm vào main.py
@app.route("/api/bds/<ma_bds>")
def get_bds_detail(ma_bds):

    lang = request.args.get("lang", "VI")

    item = BatDongSan.query.filter_by(ma_bat_dong_san=ma_bds).first()

    if not item:
        return {"error": "Không tìm thấy"}, 404

    title = item.tieu_de
    desc = item.mo_ta_chi_tiet
    loai_bds = item.loai_bat_dong_san
    loai_gd = item.loai_giao_dich
    phap_ly = item.tinh_trang_phap_ly
    so_huu = item.hinh_thuc_so_huu

    if lang != "VI":

        trans = BatDongSanTranslation.query.filter_by(
            bat_dong_san_id=item.id,
            language=lang
        ).first()

        if trans:
            if trans.tieu_de:
                title = trans.tieu_de

            if trans.mo_ta_chi_tiet:
                desc = trans.mo_ta_chi_tiet

            if trans.loai_bat_dong_san:
                loai_bds = trans.loai_bat_dong_san

            if trans.loai_giao_dich:
                loai_gd = trans.loai_giao_dich

            if trans.tinh_trang_phap_ly:
                phap_ly = trans.tinh_trang_phap_ly

            if trans.hinh_thuc_so_huu:
                so_huu = trans.hinh_thuc_so_huu

    danh_sach_anh = [img.ten_hinh_anh for img in item.danh_sach_hinh_anh]

    # Trả về CHỈ các trường có trong models.py của bạn
    return {
        "ma_bds": item.ma_bat_dong_san,
        "tieu_de": title,
        "mo_ta": desc,
        "gia": f"{item.gia_vnd:,.0f} ₫" if item.gia_vnd else "Liên hệ",

        "thanh_pho": item.thanh_pho,
        "quan_huyen": item.quan_huyen,
        "dien_tich": item.tong_dien_tich,
        "phong_ngu": item.so_phong_ngu,

        "loai_bds": loai_bds,
        "loai_gd": loai_gd,
        "phap_ly": phap_ly,
        "hinh_thuc_so_huu": so_huu,

        "so_tang": item.so_tang,
        "trang_thai": item.trang_thai,
        "ngay_dang": item.ngay_tao.strftime("%d/%m/%Y") if item.ngay_tao else "",
        "anh": danh_sach_anh
    }



@app.route("/api/thanh_pho")
def api_thanh_pho():

    ten_quoc_gia = request.args.get("quoc_gia")

    qg = QuocGia.query.filter_by(ten_quoc_gia=ten_quoc_gia).first()

    if not qg:
        return jsonify([])

    ds = ThanhPho.query.filter_by(quoc_gia_id=qg.id).all()

    data = [tp.ten_thanh_pho for tp in ds]

    return jsonify(data)

@app.route("/get_cities")
def get_cities():

    country = request.args.get("country")

    # map code -> tên trong DB
    country_map = {
        "VN": "Việt Nam",
        "JP": "Nhật Bản"
    }

    country = country_map.get(country, country)

    if not country:
        return jsonify([])

    cities = db.session.query(
        BatDongSan.thanh_pho
    ).filter(
        BatDongSan.quoc_gia == country
    ).distinct().all()

    city_list = [c[0] for c in cities if c[0]]

    return jsonify(sorted(city_list))

ADMIN_PASSWORD = "123" # Bạn nên đổi mật khẩu này hoặc để trong config.py

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    if data.get('password') == ADMIN_PASSWORD:
        return jsonify({"status": "success", "message": "Logged in"})
    return jsonify({"status": "error", "message": "Sai mật khẩu"}), 401





# Sửa lại Route hiển thị trang quản trị
@app.route('/admin/dashboard')
def admin_dashboard():
    # Gọi hàm từ database_manager chứ không phải từ đối tượng db của SQLAlchemy
    all_properties = db_mgr.get_all_properties() 
    return render_template('admin_manage.html', properties=all_properties)



# Sửa API Xóa
@app.route('/api/admin/delete/<ma_bds>', methods=['DELETE'])
def delete_property(ma_bds):
    success = db_mgr.delete_property_by_id(ma_bds)
    if success:
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 500


# API lấy dữ liệu để sửa
@app.route('/api/admin/get/<ma_bds>')
def get_property_api(ma_bds):
    item = BatDongSan.query.filter_by(ma_bat_dong_san=ma_bds).first()
    if item:
        # Lấy danh sách tên ảnh
        anh_list = [img.ten_hinh_anh for img in item.danh_sach_hinh_anh]
        
        return jsonify({
            "ma_bat_dong_san": item.ma_bat_dong_san,
            "ma_noi_bo": item.ma_noi_bo,
            "tieu_de": item.tieu_de,
            "mo_ta_chi_tiet": item.mo_ta_chi_tiet,
            "gia_vnd": item.gia_vnd,
            "gia_usd": item.gia_usd,
            "gia_jpy": item.gia_jpy,
            "gia_moi_m2": item.gia_moi_m2,
            "co_thuong_luong": item.co_thuong_luong,
            "quoc_gia": item.quoc_gia,
            "thanh_pho": item.thanh_pho,
            "quan_huyen": item.quan_huyen,
            "phuong_xa": item.phuong_xa,
            "vi_do": item.vi_do,
            "kinh_do": item.kinh_do,
            "loai_bat_dong_san": item.loai_bat_dong_san,
            "loai_giao_dich": item.loai_giao_dich,
            "tong_dien_tich": item.tong_dien_tich,
            "so_phong_ngu": item.so_phong_ngu,
            "so_phong_tam": item.so_phong_tam,
            "so_tang": item.so_tang,
            "tinh_trang_phap_ly": item.tinh_trang_phap_ly,
            "hinh_thuc_so_huu": item.hinh_thuc_so_huu,
            "trang_thai": item.trang_thai,
            "tin_noi_bat": item.tin_noi_bat,
            "images": anh_list
        })
    return jsonify({"error": "Không tìm thấy"}), 404

# Sửa API Save để nhận file
@app.route('/api/admin/save', methods=['POST'])
def save_property():
    try:
        data = json.loads(request.form.get('json_data'))
        files = request.files.getlist('images')
        
        success = db_mgr.save_property_to_db(data, files, IMAGE_FOLDER)
        
        if success:
            return jsonify({"status": "success"})
        else:
            # Thêm trường hợp thất bại
            return jsonify({"status": "error", "message": "Không thể lưu vào cơ sở dữ liệu. Vui lòng kiểm tra lại log hệ thống."}), 400
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route('/api/admin/delete_image', methods=['POST'])
def delete_image_api():
    data = request.json
    ma_bds = data.get('ma_bds')
    filename = data.get('filename')
    
    # 1. Xóa trong DB
    img_record = HinhAnhBatDongSan.query.join(BatDongSan).filter(
        BatDongSan.ma_bat_dong_san == ma_bds,
        HinhAnhBatDongSan.ten_hinh_anh == filename
    ).first()
    
    if img_record:
        db.session.delete(img_record)
        db.session.commit()
        
        # 2. Xóa file vật lý trên ổ cứng
        file_path = os.path.join(IMAGE_FOLDER, ma_bds, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

# Thêm vào file main.py

@app.route('/api/admin/delete/<ma_bds>', methods=['DELETE'])
def delete_property_api(ma_bds):
    try:
        # Gọi hàm xóa từ database_manager.py
        success = db_mgr.xoa_bat_dong_san(ma_bds)
        
        if success:
            return jsonify({"status": "success", "message": f"Đã xóa thành công BĐS {ma_bds}"})
        else:
            return jsonify({"status": "error", "message": "Không tìm thấy bất động sản hoặc có lỗi xảy ra"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)