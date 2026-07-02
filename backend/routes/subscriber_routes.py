from flask import Blueprint, jsonify, request

from backend.dao import subscriber_dao
from backend.utils import validator


subscriber_bp = Blueprint("subscriber", __name__, url_prefix="/api")


@subscriber_bp.route("/subscribers", methods=["POST"])
def create_subscriber():
    data = request.get_json()

    full_name = data.get("full_name") if data else None
    email = data.get("email") if data else None
    phone = data.get("phone") if data else None

    if validator.is_empty(full_name):
        return jsonify({"success": False, "message": "Họ tên không được để trống"}), 400

    if validator.is_empty(email):
        return jsonify({"success": False, "message": "Email không được để trống"}), 400

    if not validator.is_valid_email(email):
        return jsonify({"success": False, "message": "Email không hợp lệ"}), 400

    if not validator.is_valid_phone(phone):
        return jsonify({"success": False, "message": "Số điện thoại không hợp lệ"}), 400

    full_name = full_name.strip()
    email = email.strip().lower()
    phone = phone.strip() if not validator.is_empty(phone) else None

    if subscriber_dao.find_by_email(email):
        return jsonify({"success": False, "message": "Email đã được đăng ký"}), 400

    subscriber_dao.create_subscriber(full_name, email, phone)

    return jsonify({"success": True, "message": "Đăng ký nhận tin thành công"})


@subscriber_bp.route("/subscribers")
def get_subscribers():
    subscribers = subscriber_dao.get_all_subscribers()
    return jsonify([subscriber_dao.subscriber_to_dict(s) for s in subscribers])
