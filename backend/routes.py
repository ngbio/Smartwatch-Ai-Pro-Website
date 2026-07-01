from flask import Blueprint, jsonify, request

from .models import ContactMessage, db


api = Blueprint("api", __name__)


@api.get("/health")
def health_check():
    return jsonify({"status": "ok"})


@api.post("/contact")
def create_contact_message():
    data = request.get_json(silent=True) or {}
    required_fields = ("name", "email", "message")
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({"error": "Missing required fields", "fields": missing_fields}), 400

    contact_message = ContactMessage(
        name=data["name"].strip(),
        email=data["email"].strip(),
        message=data["message"].strip(),
    )

    db.session.add(contact_message)
    db.session.commit()

    return jsonify(contact_message.to_dict()), 201


@api.get("/contact")
def list_contact_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return jsonify([message.to_dict() for message in messages])
