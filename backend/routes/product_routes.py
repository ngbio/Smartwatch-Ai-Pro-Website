from flask import Blueprint, jsonify

from backend.dao import product_dao


product_bp = Blueprint("product", __name__, url_prefix="/api")


@product_bp.route("/product")
def get_product():
    product = product_dao.get_product_detail()

    if product is None:
        return jsonify({"message": "Không tìm thấy sản phẩm"}), 404

    return jsonify(product)


@product_bp.route("/features")
def get_features():
    features = product_dao.get_features()
    return jsonify([product_dao.feature_to_dict(f) for f in features])


@product_bp.route("/specifications")
def get_specifications():
    specifications = product_dao.get_specifications()
    return jsonify([product_dao.specification_to_dict(s) for s in specifications])
