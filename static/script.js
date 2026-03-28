const loaiGD = document.getElementById("loai_giao_dich");
const donViTien = document.getElementById("don_vi_tien");
const giaMin = document.getElementById("gia_min");
const giaMax = document.getElementById("gia_max");
const donViHienThi = document.getElementById("don_vi_hien_thi");
// Khởi tạo bản đồ tại vị trí trung tâm (Ví dụ: Hà Nội)
var map = L.map('map').setView([21.028511, 105.852020], 13);
let currentProperty = null;
let currentDetailData = null;
let isDetailOpen = false;
let propertyData = [];



const LANG_DATA = {
    VI: {
        logo_text: "REAL ESTATE PRO",
        menu_home: "Trang chủ", menu_ban: "Bán", menu_thue: "Cho thuê",
        filter_transaction: "Loại giao dịch", opt_buy: "Bán", opt_rent: "Cho thuê",
        filter_type: "Loại bất động sản", filter_country: "Quốc gia",
        filter_currency: "Tiền tệ", 
        filter_min_price: "Giá thấp nhất",
        filter_max_price: "Giá cao nhất", 
        btn_filter: "Lọc",
        placeholder_min_area: "Diện tích nhỏ nhất (m2)", 
        placeholder_max_area: "Diện tích lớn nhất (m2)",
        unit_van_yen: "Vạn Yên",
        unit_nghin_yen: "Nghìn Yên",
        opt_vn: "Việt Nam",
        opt_jp: "Nhật Bản",
        opt_nha: "Nhà",
        opt_can_ho: "Căn hộ",
        opt_dat: "Đất",
        opt_phong: "Phòng cho thuê",
        opt_nha: "Nhà",
        city: "Thành phố",
        validation_max:"Phải chọn giá max",
        back_to_list: "Quay lại danh sách",
        code: "Mã tin",
        type: "Loại hình",
        transaction: "Loại giao dịch",
        city: "Thành phố",
        district: "Quận/Huyện",
        area: "Diện tích",
        bedroom: "Phòng ngủ",
        legal: "Pháp lý",
        ownership: "Hình thức sở hữu",
        floor: "Số tầng",
        date_posted: "Ngày đăng",
        price: "Giá",
        property_specs: "Thông số bất động sản",
        property_description: "Mô tả chi tiết",
        property_images: "Hình ảnh thực tế",
        back_to_list:"Quay lại danh sách",
    },
    JP: {
        logo_text: "不動産プロ",
        menu_home: "ホーム", menu_ban: "販売", menu_thue: "賃貸",
        filter_transaction: "取引種類", opt_buy: "売買", opt_rent: "賃貸",
        filter_type: "物件種別", filter_country: "国",
        filter_currency: "通貨", filter_min_price: "最低価格",
        filter_max_price: "最高価格", btn_filter: "検索",
        placeholder_min_area: "最小面積 (m2)", placeholder_max_area: "最大面積 (m2)",
        unit_van_yen: "万円",
        unit_nghin_yen: "千円",
        opt_vn: "ベトナム",
        opt_jp: "日本",
        opt_nha: "住宅",
        opt_can_ho: "アパート",
        opt_dat: "土地",
        opt_phong: "部屋",
        city: "都市",
        validation_max:"Please select max price",
        back_to_list: "一覧に戻る",
        code: "物件ID",
        type: "タイプ",
        transaction: "取引タイプ",
        city: "都市",
        district: "地区",
        area: "面積",
        bedroom: "寝室",
        legal: "法的状況",
        ownership: "所有形態",
        floor: "階数",
        date_posted: "投稿日",
        price: "価格",
        property_specs: "物件仕様",
        property_description: "詳細な説明",
        property_images: "物件画像",
        back_to_list:"一覧に戻る",
        
    },
    EN: {
        logo_text: "REAL ESTATE PRO",
        menu_home: "Home", menu_ban: "Buy", menu_thue: "Rent",
        filter_transaction: "Transaction", opt_buy: "Buy", opt_rent: "Rent",
        filter_type: "Property Type", filter_country: "Country",
        filter_currency: "Currency", filter_min_price: "Min Price",
        filter_max_price: "Max Price", btn_filter: "Filter",
        placeholder_min_area: "Min Area (m2)", placeholder_max_area: "Max Area (m2)",
        unit_van_yen: "10k Yen",
        unit_nghin_yen: "1k Yen",
        opt_vn: "VietNam",
        opt_jp: "Japan",
        opt_nha: "House",
        opt_can_ho: "Apartment",
        opt_dat: "Land",
        opt_phong: "Room",
        city: "City",
        validation_max:"Please select max price",
        back_to_list: "Back to list",
        code: "Property ID",
        type: "Type",
        transaction: "Transaction",
        city: "City",
        district: "District",
        area: "Area",
        bedroom: "Bedrooms",
        legal: "Legal",
        ownership: "Ownership",
        floor: "Floors",
        date_posted: "Posted date",
        price: "Price",
        property_specs: "Property Specifications",
        property_description: "Detailed Description",
        property_images: "Property Images",
        back_to_list:"Back to list",
    }
};

const LANG_DICT = {

    VI:{

        back_to_list: "Quay lại danh sách",
        price: "Giá",
        area: "Diện tích",
        bedroom: "Phòng ngủ",

        property_specs: "Thông số bất động sản",
        detail_description: "Mô tả chi tiết",
        real_images: "Hình ảnh thực tế"

    },

    EN:{

        back_to_list: "Back to list",
        price: "Price",
        area: "Area",
        bedroom: "Bedrooms",

        property_specs: "Property Specifications",
        detail_description: "Detailed Description",
        real_images: "Real Images"

    },

    JP:{

        back_to_list: "一覧に戻る",
        price: "価格",
        area: "面積",
        bedroom: "寝室",

        property_specs: "不動産仕様",
        detail_description: "詳細説明",
        real_images: "実際の写真"

    }

};
function applyLanguage(lang){

    const dict = LANG_DATA[lang] || LANG_DATA.VI;

    document.querySelectorAll("[data-key]").forEach(el => {

        const key = el.dataset.key;

        if (!dict[key]) return;

        if (el.tagName === "INPUT") {
            el.placeholder = dict[key];
        } 
        else if (el.tagName === "OPTION") {
            el.textContent = dict[key];
        }
        else {
            el.textContent = dict[key];
        }

    });

}

function changeLanguage(lang) {
    localStorage.setItem("lang", lang);   // lưu ngôn ngữ

    const url = new URL(window.location.href);

    const currentLang = url.searchParams.get("lang") || "VI";

    if(currentLang === lang){
        return;
    }

    localStorage.setItem("selected_language", lang);

    url.searchParams.set("lang", lang);

    window.location.href = url.toString();
}

function formatCurrency(val, currencyCode) {
    if (val === 0) return "0";
    if (!val) return "";

    // Cấu hình định dạng theo từng loại tiền
    let locale = 'vi-VN';
    if (currencyCode === 'JPY') locale = 'ja-JP';
    if (currencyCode === 'USD') locale = 'en-US';

    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currencyCode,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(val);
}

function capNhatGia() {
    const loai = loaiGD.value;
    const tien = donViTien.value; // VND, JPY, hoặc USD
    const lang = localStorage.getItem("selected_language") || "VI";
    const dict = LANG_DATA[lang] || LANG_DATA.VI;

    giaMin.innerHTML = `<option value="">${dict.filter_min_price}</option>`;
    giaMax.innerHTML = `<option value="">${dict.filter_max_price}</option>`;
    if (!loai || !tien) return;

    // Lấy dữ liệu từ FILTER_DATA (được render từ main.py)
    const data = FILTER_DATA.tien_te[tien][loai];

    // Điền dữ liệu vào Min Price
    data.min.forEach(val => {
        let opt = document.createElement("option");
        opt.value = val;
        opt.textContent = formatCurrency(val, tien);
        if (String(SELECTED_FILTERS.gia_min) === String(val)) opt.selected = true;
        giaMin.appendChild(opt);
    });

    // Điền dữ liệu vào Max Price
    data.max.forEach(val => {
        let opt = document.createElement("option");
        opt.value = val;
        opt.textContent = formatCurrency(val, tien);
        if (String(SELECTED_FILTERS.gia_max) === String(val)) opt.selected = true;
        giaMax.appendChild(opt);
    });
}


function focusMarker(ma_bds){

    if(!window.propertyData) return;

    const item = propertyData.find(p => p.ma_bds === ma_bds);

    if(!item) return;

    if(item.vi_do && item.kinh_do){

        map.setView([item.vi_do, item.kinh_do], 16, {
            animate: true
        });

    }
}

/* VALIDATION */
document.getElementById("filterForm").addEventListener("submit", function(e) {

    let min = giaMin.value;
    let max = giaMax.value;
    let tien = donViTien.value;

    if (min && !max) {
        alert(langDict.validation_max);
        e.preventDefault();
        return;
    }

    if (min && max && parseFloat(max) <= parseFloat(min)) {
        alert("Gia max phai lon hon gia min");
        e.preventDefault();
        return;
    }

    if ((min || max) && !tien) {
        alert("Phai chon don vi tien");
        e.preventDefault();
        return;
    }

    const formData = new FormData(this);
    let filterValues = {};

    formData.forEach((value, key) => {
        if (value !== "")
            filterValues[key] = value;
    });

    console.log("Filter:", filterValues);
});


const langItems = document.querySelectorAll(".lang-item");

langItems.forEach(item => {
    item.addEventListener("click", function() {

        // bỏ active cũ
        langItems.forEach(el => el.classList.remove("active"));

        // active mới
        this.classList.add("active");

        let selectedLang = this.dataset.lang;

        // lưu vào localStorage
        localStorage.setItem("selected_language", selectedLang);

        console.log("Ngon ngu da chon:", selectedLang);

        // Có thể reload trang nếu muốn
        // location.reload();
    });
});

// Khi load trang, đọc lại ngôn ngữ đã chọn
window.addEventListener("load", function() {

    let savedLang = localStorage.getItem("selected_language");

    if (savedLang) {
        langItems.forEach(el => {
            if (el.dataset.lang === savedLang) {
                el.classList.add("active");
            }
        });
    }
});




document.addEventListener("DOMContentLoaded", () => {

    const url = new URL(window.location.href);
    const lang = url.searchParams.get("lang") || "VI";

    applyLanguage(lang);

    capNhatGia(); 
    loaiGD.addEventListener("change", capNhatGia);
});

// Biến toàn cục để quản lý Gallery phóng to
let currentAlbum = [];
let currentIndex = 0;


async function showDetail(maBDS) {

    currentDetailData = maBDS;
    isDetailOpen = true;

    // cập nhật URL
    const url = new URL(window.location);
    url.searchParams.set("bds", maBDS);
    window.history.replaceState({}, "", url);

    document.getElementById('list-view').style.display = 'none';




    currentDetailData = maBDS;
    isDetailOpen = true;

    
    document.getElementById('list-view').style.display = 'none';
    const detailView = document.getElementById('detail-view');
    const detailContent = document.getElementById('detail-content');

    
    const lang = localStorage.getItem("selected_language") || "VI";
    const dict = LANG_DATA[lang] || LANG_DATA.VI;

    
    
    detailView.style.display = 'block';
    detailContent.innerHTML = "<div class='loading'>Đang tải thông tin chi tiết...</div>";


    // Thêm logic di chuyển bản đồ
    const item = window.propertyData.find(p => p.ma_bds === maBDS);
    if (item && item.vi_do && item.kinh_do) {
        map.flyTo([item.vi_do, item.kinh_do], 16, {
            animate: true,
            duration: 1.5
        });
        
        // Mở popup tương ứng trên bản đồ (tùy chọn)
        map.eachLayer(layer => {
            if (layer instanceof L.Marker && layer.getLatLng().lat === item.vi_do) {
                layer.openPopup();
            }
        });
    }
    try {
        const lang = localStorage.getItem("selected_language") || "VI";
        const response = await fetch(`/api/bds/${maBDS}?lang=${lang}`);
        const data = await response.json();

        if (data.error) {
            detailContent.innerHTML = `<p>${data.error}</p>`;
            return;
        }

        // Lưu danh sách ảnh vào biến toàn cục (lọc trùng tên)
        currentAlbum = [...new Set(data.anh)].map(fileName => `/property_images/${data.ma_bds}/${fileName}`);

        // Tạo HTML cho danh sách ảnh thu nhỏ
        let imagesHtml = '<div class="detail-gallery-grid">';
        currentAlbum.forEach((src, index) => {
            imagesHtml += `
                <div class="detail-img-item" onclick="openImageModal(${index})">
                    <img src="${src}" alt="${data.tieu_de}" />
                </div>`;
        });
        imagesHtml += '</div>';

        // Đổ dữ liệu vào giao diện (Thông tin -> Mô tả -> Ảnh)
        detailContent.innerHTML = `
            <div class="property-detail-wrapper">
                <h1 class="detail-title">${data.tieu_de}</h1>
                <p class="detail-location"><i class="fa-solid fa-location-dot"></i> ${data.quan_huyen}, ${data.thanh_pho}</p>
                
                <div class="detail-main-stats">
                    <div class="stat-item"><span>${dict.price}</span><strong>${data.gia}</strong></div>
                    <div class="stat-item"><span>${dict.area}</span><strong>${data.dien_tich} m²</strong></div>
                    <div class="stat-item"><span>${dict.bedroom}</span><strong>${data.phong_ngu}</strong></div>
                </div>

                <div class="detail-info-grid">
                    <h3>${dict.property_specs}</h3>
                    <ul>
                        <li><strong>${dict.code}:</strong> ${data.ma_bds}</li>
                        <li><strong>${dict.type}:</strong> ${data.loai_bds}</li>
                        <li><strong>${dict.transaction}:</strong> ${data.loai_gd}</li>
                        <li><strong>${dict.legal}:</strong> ${data.phap_ly}</li>
                        <li><strong>${dict.ownership}:</strong> ${data.hinh_thuc_so_huu}</li>
                        <li><strong>${dict.floor}:</strong> ${data.so_tang}</li>
                        <li><strong>${dict.date_posted}:</strong> ${data.ngay_dang}</li>
                    </ul>
                </div>

                <div class="detail-description" style="margin-top: 25px;">
                    <h3>${dict.property_description}</h3>
                    <p style="white-space: pre-wrap; line-height: 1.6; color: #444;">${data.mo_ta}</p>
                </div>

                <hr style="margin: 30px 0; border: 0; border-top: 1px solid #eee;">

                <div class="detail-image-section">
                    <h3>${dict.property_images}</h3>
                    ${imagesHtml}
                </div>
            </div>

            <div id="imageModal" class="image-modal">
                <span class="close-modal" onclick="closeImageModal()">&times;</span>
                <button class="modal-prev" onclick="changeImage(-1)">&#10094;</button>
                <img class="modal-content" id="imgModalContent">
                <button class="modal-next" onclick="changeImage(1)">&#10095;</button>
                <div id="caption" style="position:absolute; bottom:20px; color:white;"></div>
            </div>
        `;

    } catch (error) {
        console.error("Lỗi:", error);
        detailContent.innerHTML = "<p>Lỗi kết nối máy chủ.</p>";
    }
}

// Hàm mở Modal và gán index hiện tại
function openImageModal(index) {
    currentIndex = index;
    const modal = document.getElementById("imageModal");
    modal.style.display = "flex";
    updateModalImage();
}

// Hàm cập nhật ảnh trong Modal
function updateModalImage() {
    const modalImg = document.getElementById("imgModalContent");
    const caption = document.getElementById("caption");
    modalImg.src = currentAlbum[currentIndex];
    caption.innerText = `Ảnh ${currentIndex + 1} / ${currentAlbum.length}`;
}

// Hàm chuyển ảnh
function changeImage(step) {
    currentIndex += step;
    // Vòng lặp: nếu quá ảnh cuối thì về ảnh đầu và ngược lại
    if (currentIndex >= currentAlbum.length) currentIndex = 0;
    if (currentIndex < 0) currentIndex = currentAlbum.length - 1;
    updateModalImage();
}

function closeImageModal() {
    document.getElementById("imageModal").style.display = "none";
}

// Thêm sự kiện bàn phím (Mũi tên trái/phải để chuyển ảnh, Esc để đóng)
document.addEventListener('keydown', function(e) {
    const modal = document.getElementById("imageModal");
    if (modal && modal.style.display === "flex") {
        if (e.key === "ArrowLeft") changeImage(-1);
        if (e.key === "ArrowRight") changeImage(1);
        if (e.key === "Escape") closeImageModal();
    }
});

function hideDetail() {
    document.getElementById('list-view').style.display = 'grid';
    document.getElementById('detail-view').style.display = 'none';

    isDetailOpen = false;

    const url = new URL(window.location);
    url.searchParams.delete("bds");
    window.history.replaceState({}, "", url);
    
}

const countrySelect = document.getElementById("ten_quoc_gia");
const citySelect = document.getElementById("ten_thanh_pho");

countrySelect.addEventListener("change", function(){

    const country = this.value;

    const lang = localStorage.getItem("selected_language") || "VI";
    const dict = LANG_DATA[lang] || LANG_DATA.VI;

    citySelect.innerHTML = `<option value="">${dict.city}</option>`;

    if(!country) return;

    fetch(`/get_cities?country=${country}`)
    .then(res => res.json())
    .then(data => {

        data.forEach(city => {

            const opt = document.createElement("option");
            opt.value = city;
            opt.textContent = city;

            citySelect.appendChild(opt);

        });

    });

});
// element

function updatePriceFilter(){

    const loaiSelect = document.getElementById("loai_giao_dich")
    const tienSelect = document.getElementById("don_vi_tien")

    const loai = loaiSelect.value
    const tien = tienSelect.value

    if(!loai || !tien) return

    const data = FILTER_DATA.tien_te[tien][loai]

    if(!data) return

    const minSelect = document.getElementById("gia_min")
    const maxSelect = document.getElementById("gia_max")

    const lang = localStorage.getItem("selected_language") || "VI";
    const dict = LANG_DATA[lang] || LANG_DATA.VI;

    minSelect.innerHTML = `<option value="">${dict.filter_min_price}</option>`;
    maxSelect.innerHTML = `<option value="">${dict.filter_max_price}</option>`;

    data.min.forEach(price => {

        const op = document.createElement("option")
        op.value = price
        op.textContent = price.toLocaleString()

        minSelect.appendChild(op)

    })

    data.max.forEach(price => {

        const op = document.createElement("option")
        op.value = price
        op.textContent = price.toLocaleString()

        maxSelect.appendChild(op)

    })
    // console.log("loai:", loai)
    // console.log("tien:", tien)
    // console.log("data:", data)


    // selected_filters
}

document.getElementById("loai_giao_dich")
.addEventListener("change", updatePriceFilter)

document.getElementById("don_vi_tien")
.addEventListener("change", updatePriceFilter)

window.addEventListener("DOMContentLoaded", updatePriceFilter)







// Hàm để thêm các Marker từ danh sách BDS
function displayMarkers(properties) {
    properties.forEach(item => {
        if (item.vi_do && item.kinh_do) {
            // Tạo một marker
            var marker = L.marker([item.vi_do, item.kinh_do]).addTo(map);
            
            // Nội dung khi click vào ghim (Popup)
            var popupContent = `
                <div class="map-popup">
                    <img src="${item.anh_bia}" style="width:100px; height:auto;">
                    <h4>${item.tieu_de}</h4>
                    <p style="color: red; font-weight: bold;">${item.gia}</p>
                    <a href="#" onclick="showDetail('${item.ma_bds}')">Xem chi tiết</a>
                </div>
            `;
            marker.bindPopup(popupContent);
        }
    });
}


// Thêm bản đồ nền (Layer)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Hàm vẽ các ghim giá tiền
function renderMarkers(data) {
    // 1. Xóa tất cả Marker cũ trên bản đồ (tránh trùng lặp khi lọc)
    map.eachLayer(function(layer){
        if(layer instanceof L.Marker){
            map.removeLayer(layer);
        }
    });

    if (!data || data.length === 0) return;

    // 2. Tạo nhóm các điểm để sau này tự động căn chỉnh khung hình (fitBounds)
    const points = [];

    data.forEach(item => {
        if (item.vi_do && item.kinh_do) {
            // Tạo Icon tùy chỉnh hiển thị giá
            var priceIcon = L.divIcon({
                className: "price-marker",
                html: `
                    <div class="price-label">${item.gia}</div>
                    <div class="price-dot"></div>
                `,
                iconSize: [80, 40],
                iconAnchor: [40, 20]
            });

            var marker = L.marker([item.vi_do, item.kinh_do], {icon: priceIcon}).addTo(map);

            // Nội dung Popup khi click vào giá trên bản đồ
            marker.bindPopup(`
                <div style="width:150px; cursor:pointer" onclick="showDetail('${item.ma_bds}')">
                    <img src="/property_images/${item.ma_bds}/${item.anh}" style="width:100%; border-radius:5px">
                    <h5 style="margin:5px 0; font-size:13px">${item.tieu_de}</h5>
                    <b style="color:#d63031">${item.gia}</b>
                </div>
            `);
            
            points.push([item.vi_do, item.kinh_do]);
        }
    });

    // 3. Tự động Zoom bản đồ để bao quát tất cả các điểm đang hiển thị
    if (points.length > 0) {
        map.fitBounds(points, { padding: [50, 50] });
    }
}

// Chạy hàm vẽ ghim với dữ liệu từ Backend
renderMarkers(propertyData);

function updateList(data){

    const container = document.getElementById("list-view");

    if(!container){
        console.warn("list-view not found");
        return;
    }

    container.innerHTML = "";

    if(!data || data.length === 0){
        container.innerHTML = `
        <div class="no-result">
            <i class="fa-solid fa-circle-exclamation"></i>
            <p>Không tìm thấy bất động sản</p>
        </div>
        `;
        return;
    }

    data.forEach(item => {

        const html = `
        <div class="property-card"
            data-id="${item.ma_bds}"
            onmouseenter="focusMarker('${item.ma_bds}')"
            onclick="showDetail('${item.ma_bds}')">

            <div class="property-image">
                <img src="/property_images/${item.ma_bds}/${item.anh}">
            </div>

            <div class="property-info">
                <h3 class="property-title">${item.tieu_de}</h3>
                <p class="property-price">${item.gia}</p>
                <p class="property-location">${item.ten_thanh_pho}</p>
            </div>

        </div>
        `;

        container.innerHTML += html;

    });

}

// nếu URL có bds thì mở chi tiết
const params = new URLSearchParams(window.location.search);
const bdsID = params.get("bds");

if (bdsID) {
    showDetail(bdsID);
}

document.addEventListener("DOMContentLoaded", function () {

    const savedLang = localStorage.getItem("lang") || "VI";

    changeLanguage(savedLang);

    // Thêm dòng này:
    if (window.propertyData) {
        renderMarkers(window.propertyData);
    }

});

// Khai báo biến layer ở đầu file script.js
var map = L.map('map').setView([21.028511, 105.852020], 13);
let currentTileLayer;

// Hàm để thay đổi ngôn ngữ bản đồ
function updateMapLanguage(lang) {
    // Xóa layer cũ nếu có
    if (currentTileLayer) {
        map.removeLayer(currentTileLayer);
    }

    let tileUrl;
    
    // Sử dụng CartoDB (Miễn phí, hỗ trợ đa ngôn ngữ tốt và sạch sẽ)
    // Nếu bạn có Mapbox Token thì dùng Mapbox sẽ chuẩn xác nhất
    switch(lang) {
        case 'EN':
            tileUrl = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png'; 
            // Lưu ý: Các dịch vụ miễn phí thường hiển thị tên quốc tế (English) mặc định
            break;
        case 'JP':
            // Sử dụng OpenStreetMap phiên bản tiếng Nhật nếu có, 
            // hoặc dùng CartoDB với nhãn tiếng Nhật
            tileUrl = 'https://{s}.tile.openstreetmap.jp/{z}/{x}/{y}.png';
            break;
        default: // VI
            tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    }

    currentTileLayer = L.tileLayer(tileUrl, {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
}


function showLoginForm() {
    document.getElementById('loginModal').style.display = 'block';
}

function handleLogin() {
    const pwd = document.getElementById('adminPassword').value;
    fetch('/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: pwd })
    })
    .then(res => {
        if (res.ok) {
            window.location.href = '/admin/dashboard'; // Chuyển sang trang quản trị
        } else {
            alert("Mật khẩu không đúng!");
        }
    });
}