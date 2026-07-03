from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from backend.dao import chat_history_dao
from backend.utils import ai_client, validator


chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/api")


@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message")
    session_id = data.get("session_id")

    if validator.is_empty(message):
        return jsonify({"success": False, "message": "Nội dung chat không được để trống"}), 400

    message = message.strip()
    session_id = session_id.strip() if not validator.is_empty(session_id) else "anonymous"

    reply = ai_client.generate_reply(message)

    try:
        chat_history_dao.save_chat(session_id, None, message, reply)
    except SQLAlchemyError as ex:
        print(f"Database error while saving chatbot history: {ex}")

    return jsonify({"reply": reply})


@chatbot_bp.route("/chat/history")
def get_chat_history():
    try:
        history = chat_history_dao.get_chat_history()
    except SQLAlchemyError as ex:
        print(f"Database error while loading chatbot history: {ex}")
        return jsonify([])

    return jsonify([chat_history_dao.chat_to_dict(c) for c in history])
