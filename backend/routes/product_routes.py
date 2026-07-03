from flask import Blueprint, jsonify
from sqlalchemy.exc import SQLAlchemyError

from backend.dao import product_dao


product_bp = Blueprint("product", __name__, url_prefix="/api")

DEFAULT_PRODUCT = {
    "name": "SmartWatch AI Pro",
    "subtitle": "Đồng hồ AI chăm sóc sức khỏe thông minh",
    "description": "Theo dõi sức khỏe, luyện tập và giấc ngủ bằng AI.",
    "price": "3.990.000đ",
    "image": "",
    "image_url": "",
    "features": [
        {
            "title": "AI Health Tracking",
            "description": "Theo dõi sức khỏe bằng AI theo thời gian thực.",
            "icon": "AI",
        },
        {
            "title": "GPS",
            "description": "Định vị chính xác khi chạy bộ, đạp xe và luyện tập ngoài trời.",
            "icon": "GPS",
        },
        {
            "title": "Fast Charging",
            "description": "Sạc nhanh, phù hợp với lịch trình bận rộn hằng ngày.",
            "icon": "FC",
        },
        {
            "title": "Waterproof",
            "description": "Chống nước chuẩn IP68 cho nhu cầu sinh hoạt hằng ngày.",
            "icon": "IP",
        },
    ],
    "specifications": [
        {"name": "Màn hình", "value": "AMOLED 1.8 inch"},
        {"name": "Pin", "value": "500mAh"},
        {"name": "Bluetooth", "value": "5.3"},
        {"name": "Chống nước", "value": "IP68"},
    ],
}


@product_bp.route("/product")
def get_product():
    try:
        product = product_dao.get_product_detail()
    except SQLAlchemyError as ex:
        print(f"Database error while loading product: {ex}")
        return jsonify(DEFAULT_PRODUCT)

    if product is None:
        return jsonify(DEFAULT_PRODUCT)

    return jsonify({**DEFAULT_PRODUCT, **product})


@product_bp.route("/features")
def get_features():
    try:
        features = product_dao.get_features()
    except SQLAlchemyError as ex:
        print(f"Database error while loading features: {ex}")
        return jsonify(DEFAULT_PRODUCT["features"])

    return jsonify([product_dao.feature_to_dict(f) for f in features])


@product_bp.route("/specifications")
def get_specifications():
    try:
        specifications = product_dao.get_specifications()
    except SQLAlchemyError as ex:
        print(f"Database error while loading specifications: {ex}")
        return jsonify(DEFAULT_PRODUCT["specifications"])

    return jsonify([product_dao.specification_to_dict(s) for s in specifications])
