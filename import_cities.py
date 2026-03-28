import os
from models import db, QuocGia, ThanhPho
from main import app


FILE_PATH = "data/cities5000.txt"
COUNTRY_CODE = "JP"
TEN_QUOC_GIA = "Nhật Bản"

# COUNTRY_CODE = "VN"
# TEN_QUOC_GIA = "Việt Nam"


def import_thanh_pho():
    with app.app_context():

        # Kiểm tra quốc gia
        qg = QuocGia.query.filter_by(ten_quoc_gia=TEN_QUOC_GIA).first()

        if not qg:
            qg = QuocGia(ten_quoc_gia=TEN_QUOC_GIA)
            db.session.add(qg)
            db.session.commit()

        count = 0

        with open(FILE_PATH, encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")

                country_code = parts[8]

                if country_code == COUNTRY_CODE:

                    alternates = parts[3].split(",")

                    ten_thanh_pho = parts[1]
                    if COUNTRY_CODE == "VN":
                        for name in alternates:
                            if " " in name and any(ord(c) > 127 for c in name):
                                ten_thanh_pho = name
                                break
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

        print("Da import", count, "thanh pho cho", TEN_QUOC_GIA)


if __name__ == "__main__":
    import_thanh_pho()