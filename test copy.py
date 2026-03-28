from database_manager import *
import time
from datetime import datetime


# Tạo bảng
# xoa_toan_bo_bang()
# tao_bang()
xoa_bat_dong_san("BDS100")
# xoa_bat_dong_san("BDS100")
# Thêm dữ liệu
# them_bat_dong_san(
#     ma_bat_dong_san="BDS100",
#     ma_noi_bo="BDS100",
#     tieu_de="Bán nhà trung tâm Hà Nội",
#     mo_ta_chi_tiet=" - Nhà 4 tầng. Có ban công. 4 phòng ngủ, 2 phòng khách.\n - Liên hệ theo số điện thoại: 12358910",
#     gia_vnd=4500000000,
#     quoc_gia = "Việt Nam",
#     thanh_pho="Hà Nội",
#     quan_huyen="Hoàn Kiếm",
#     tong_dien_tich = 100,
#     so_phong_ngu = 4,
#     so_tang = 4,
#     loai_bat_dong_san="Nhà",
#     loai_giao_dich="Bán",
#     vi_do = 21.028511,
#     kinh_do = 105.852020,
#     tinh_trang_phap_ly="Sổ đỏ",
#     hinh_thuc_so_huu="Mãi mãi",
#     trang_thai="Còn bán",
#     tin_noi_bat=True,
#     luot_xem=10,
#     ngay_tao=datetime.now(),
#     ngay_cap_nhat=datetime.now()
# )
# them_hinh_anh_cho_bds(
#     "BDS100",
#     [
#         "anh1.jpg",
#         "anh2.jpg",
#         "anh3.jpg"
#     ]
# )

# them_bat_dong_san(
#     ma_bat_dong_san="BDS110",
#     ma_noi_bo="BDS110",
#     tieu_de="Bán nhà trung tâm Hà Nội",
#     mo_ta_chi_tiet=" - Nhà 4 tầng. Có ban công. 4 phòng ngủ, 2 phòng khách.\n - Liên hệ theo số điện thoại: 12358910",
#     gia_vnd=4500000000,
#     quoc_gia = "Việt Nam",
#     thanh_pho="Hải Dương",
#     quan_huyen="Cẩm Giàng",
#     tong_dien_tich = 100,
#     so_phong_ngu = 4,
#     so_tang = 4,
#     loai_bat_dong_san="Nhà",
#     loai_giao_dich="Bán",
#     vi_do = 21.038511,
#     kinh_do = 105.852020,
#     tinh_trang_phap_ly="Sổ đỏ",
#     hinh_thuc_so_huu="Mãi mãi",
#     trang_thai="Còn bán",
#     tin_noi_bat=True,
#     luot_xem=10,
#     ngay_tao=datetime.now(),
#     ngay_cap_nhat=datetime.now()
# )
# them_hinh_anh_cho_bds(
#     "BDS110",
#     [
#     ]
# )

# them_ban_dich(
#     ma_bds="BDS110",
#     language="EN",
#     tieu_de="House for sale in central Hanoi",
#     mo_ta_chi_tiet="4-floor house with balcony. 4 bedrooms, 2 living rooms.\n - Contact us by phone.: 12358910",
#     loai_bat_dong_san="House",
#     loai_giao_dich="Sale",
#     tinh_trang_phap_ly="Red book",
#     hinh_thuc_so_huu="Permanent"
# )

# them_ban_dich(
#     ma_bds="BDS110",
#     language="JP",
#     tieu_de="ハノイ中心部で販売中の住宅",
#     mo_ta_chi_tiet="バルコニー付きの4階建て住宅。ベッドルーム4室、リビングルーム2室。\n - お電話にてお問い合わせください。: 12358910",
#     loai_bat_dong_san="家",
#     loai_giao_dich="販売",
#     tinh_trang_phap_ly="レッドブック",
#     hinh_thuc_so_huu="永続"
# )

# them_ban_dich(
#     ma_bds="BDS100",
#     language="EN",
#     tieu_de="House for sale in central Hanoi",
#     mo_ta_chi_tiet="4-floor house with balcony. 4 bedrooms, 2 living rooms.\n - Contact us by phone.: 12358910",
#     loai_bat_dong_san="House",
#     loai_giao_dich="Sale",
#     tinh_trang_phap_ly="Red book",
#     hinh_thuc_so_huu="Permanent"
# )

# them_ban_dich(
#     ma_bds="BDS100",
#     language="JP",
#     tieu_de="ハノイ中心部で販売中の住宅",
#     mo_ta_chi_tiet="バルコニー付きの4階建て住宅。ベッドルーム4室、リビングルーム2室。\n - お電話にてお問い合わせください。: 12358910",
#     loai_bat_dong_san="家",
#     loai_giao_dich="販売",
#     tinh_trang_phap_ly="レッドブック",
#     hinh_thuc_so_huu="永続"
# )


# # hien_thi_hinh_anh("BDS100")

# # # In danh sách
# # for bds in lay_danh_sach():
# #     print(bds.ma_bat_dong_san, bds.tieu_de)

# # # Cập nhật
# # cap_nhat_bat_dong_san("BDS100", gia=5000000000)

# # # Tăng lượt xem
# # tang_luot_xem("BDS100")

# # # Xóa
# # # xoa_bat_dong_san("BDS100")

# #

# # In danh sách
# print("------------------")
# for bds in lay_danh_sach():
#     print(bds.ma_bat_dong_san, bds.so_tang, bds.gia_vnd, bds.loai_giao_dich, bds.loai_bat_dong_san, 
#           bds.thanh_pho, bds.quoc_gia, bds.tong_dien_tich, bds.so_phong_ngu, bds.tinh_trang_phap_ly, bds.hinh_thuc_so_huu,
#           bds.trang_thai, bds.tin_noi_bat, bds.luot_xem, bds.ngay_tao, bds.ngay_cap_nhat)