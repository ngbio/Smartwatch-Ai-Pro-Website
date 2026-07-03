from backend import db
from backend.models import ChatMessage


def save_chat(session_id, product_id, question, answer):
    chat = ChatMessage(
        session_id=session_id,
        product_id=product_id,
        question=question,
        answer=answer,
    )

    db.session.add(chat)
    db.session.commit()

    return chat


def get_chat_history():
    return ChatMessage.query.order_by(ChatMessage.created_at.desc()).all()


def chat_to_dict(chat):
    return {
        "id": chat.id,
        "session_id": chat.session_id,
        "product_id": chat.product_id,
        "question": chat.question,
        "answer": chat.answer,
        "created_at": chat.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
