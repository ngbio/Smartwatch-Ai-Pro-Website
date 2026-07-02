from datetime import datetime

from sqlalchemy import Column, DateTime, Double, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend import db


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Product(BaseModel):
    __tablename__ = "product"

    name = Column(String(120), nullable=False)
    subtitle = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Double, nullable=True)
    image = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    features = relationship("Feature", backref="product", lazy=True)
    specifications = relationship("Specification", backref="product", lazy=True)
    subscribers = relationship("Subscriber", backref="product", lazy=True)
    chat_messages = relationship("ChatMessage", backref="product", lazy=True)

    def __str__(self):
        return self.name


class Feature(BaseModel):
    __tablename__ = "feature"

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    title = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(80), nullable=True)

    def __str__(self):
        return self.title


class Specification(BaseModel):
    __tablename__ = "specification"

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    name = Column(String(120), nullable=False)
    value = Column(String(255), nullable=False)

    def __str__(self):
        return f"{self.name}: {self.value}"


class Subscriber(BaseModel):
    __tablename__ = "subscriber"

    product_id = Column(Integer, ForeignKey("product.id"), nullable=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(30), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    def __str__(self):
        return self.full_name


class ChatMessage(BaseModel):
    __tablename__ = "chat_message"

    session_id = Column(String(120), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class ContactMessage(BaseModel):
    __tablename__ = "contact_messages"

    name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
        }
