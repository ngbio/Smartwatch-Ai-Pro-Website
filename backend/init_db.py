try:
    from backend import AIVEN_DB_HOST, AIVEN_DB_NAME, app, db
    from backend.models import ChatMessage, Feature, Product, Specification, Subscriber
except ModuleNotFoundError:
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from backend import AIVEN_DB_HOST, AIVEN_DB_NAME, app, db
    from backend.models import ChatMessage, Feature, Product, Specification, Subscriber


def create_sample_product():
    product_data = {
        "name": "SmartWatch AI Pro",
        "subtitle": "Đồng hồ AI chăm sóc sức khỏe thông minh",
        "description": "Theo dõi sức khỏe, luyện tập và giấc ngủ bằng AI.",
        "price": 3990000,
        "image": "https://res.cloudinary.com/dprwsgoeg/image/upload/v1783053621/ChatGPT_Image_Jul_3_2026_11_39_56_AM_dxtlr5.png",
    }

    features = [
        {
            "title": "AI Health Tracking",
            "description": "Theo dõi sức khỏe bằng AI theo thời gian thực.",
            "icon": "heart",
        },
        {
            "title": "GPS",
            "description": "Định vị chính xác khi chạy bộ, đạp xe và luyện tập ngoài trời.",
            "icon": "map-pin",
        },
        {
            "title": "Fast Charging",
            "description": "Sạc nhanh, phù hợp với lịch trình bận rộn hằng ngày.",
            "icon": "battery-charging",
        },
        {
            "title": "Waterproof",
            "description": "Chống nước chuẩn IP68 cho nhu cầu sinh hoạt hằng ngày.",
            "icon": "droplets",
        },
    ]

    specifications = [
        {"name": "Màn hình", "value": "AMOLED 1.8 inch"},
        {"name": "Pin", "value": "500mAh"},
        {"name": "Bluetooth", "value": "5.3"},
        {"name": "Chống nước", "value": "IP68"},
    ]

    product = Product.query.filter(Product.name == product_data["name"]).first()

    if product is None:
        product = Product(**product_data)
        db.session.add(product)
        db.session.flush()
    else:
        product.subtitle = product_data["subtitle"]
        product.description = product_data["description"]
        product.price = product_data["price"]
        product.image = product_data["image"]

    Feature.query.filter(Feature.product_id == product.id).delete()
    Specification.query.filter(Specification.product_id == product.id).delete()

    db.session.add_all([Feature(product_id=product.id, **feature) for feature in features])
    db.session.add_all(
        [
            Specification(product_id=product.id, **specification)
            for specification in specifications
        ]
    )

    return product


def remove_extra_products(main_product):
    extra_products = Product.query.filter(Product.id != main_product.id).all()

    for product in extra_products:
        Feature.query.filter(Feature.product_id == product.id).delete()
        Specification.query.filter(Specification.product_id == product.id).delete()
        Subscriber.query.filter(Subscriber.product_id == product.id).update(
            {"product_id": main_product.id}
        )
        ChatMessage.query.filter(ChatMessage.product_id == product.id).update(
            {"product_id": main_product.id}
        )
        db.session.delete(product)


def create_sample_subscribers(product):
    subscribers = [
        {
            "full_name": "Nguyen Van A",
            "email": "vana@gmail.com",
            "phone": "0901234567",
        },
        {
            "full_name": "Tran Thi B",
            "email": "thib@gmail.com",
            "phone": "0912345678",
        },
    ]

    for item in subscribers:
        existed = Subscriber.query.filter(Subscriber.email == item["email"]).first()
        if not existed:
            db.session.add(Subscriber(product_id=product.id, **item))


def create_sample_chat_history(product):
    existed = ChatMessage.query.first()

    if existed:
        return

    db.session.add(
        ChatMessage(
            session_id="sample-session",
            product_id=product.id,
            question="Đồng hồ này chống nước không?",
            answer="SmartWatch AI Pro chống nước chuẩn IP68 cho nhu cầu sinh hoạt hằng ngày.",
        )
    )


def create_sample_data():
    product = create_sample_product()
    remove_extra_products(product)
    create_sample_subscribers(product)
    create_sample_chat_history(product)


def init_db():
    with app.app_context():
        print(f"Using database: {AIVEN_DB_NAME} on {AIVEN_DB_HOST}")
        db.create_all()
        create_sample_data()
        db.session.commit()
        print(f"Products: {Product.query.count()}")
        print(f"Features: {Feature.query.count()}")
        print(f"Specifications: {Specification.query.count()}")
        print(f"Subscribers: {Subscriber.query.count()}")
        print(f"Chat messages: {ChatMessage.query.count()}")


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
