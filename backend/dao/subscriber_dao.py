from backend import db
from backend.models import Subscriber


def create_subscriber(full_name, email, phone=None):
    subscriber = Subscriber(
        full_name=full_name,
        email=email,
        phone=phone,
    )

    db.session.add(subscriber)
    db.session.commit()

    return subscriber


def find_by_email(email):
    return Subscriber.query.filter(Subscriber.email == email).first()


def get_all_subscribers():
    return Subscriber.query.order_by(Subscriber.created_at.desc()).all()


def subscriber_to_dict(subscriber):
    return {
        "id": subscriber.id,
        "full_name": subscriber.full_name,
        "email": subscriber.email,
        "phone": subscriber.phone,
        "created_at": subscriber.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
