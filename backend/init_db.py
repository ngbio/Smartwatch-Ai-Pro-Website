try:
    from backend import app, db
    from backend.models import ChatMessage, Feature, Product, Specification, Subscriber
except ModuleNotFoundError:
    from pathlib import Path
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from backend import app, db
    from backend.models import ChatMessage, Feature, Product, Specification, Subscriber


def create_sample_product():
    products = [
        {
            "product": {
                "name": "SmartWatch AI Pro",
                "subtitle": "Đồng hồ AI chăm sóc sức khỏe thông minh",
                "description": "Theo dõi sức khỏe, luyện tập và giấc ngủ bằng AI.",
                "price": 3990000,
                "image": "/images/watch.png",
            },
            "features": [
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
            ],
            "specifications": [
                {"name": "Màn hình", "value": "AMOLED 1.8 inch"},
                {"name": "Pin", "value": "500mAh"},
                {"name": "Bluetooth", "value": "5.3"},
                {"name": "Chống nước", "value": "IP68"},
            ],
        },
        {
            "product": {
                "name": "SmartWatch Sport X",
                "subtitle": "Đồng hồ thể thao GPS cho luyện tập ngoài trời",
                "description": "Theo dõi bài tập, nhịp tim và quãng đường với GPS chính xác.",
                "price": 2990000,
                "image": "/images/watch-sport.png",
            },
            "features": [
                {
                    "title": "Sport Mode",
                    "description": "Hỗ trợ nhiều chế độ luyện tập như chạy bộ, đạp xe và bơi.",
                    "icon": "activity",
                },
                {
                    "title": "GPS Tracking",
                    "description": "Ghi lại cung đường và tốc độ luyện tập.",
                    "icon": "map",
                },
                {
                    "title": "Heart Rate",
                    "description": "Theo dõi nhịp tim liên tục khi vận động.",
                    "icon": "heart-pulse",
                },
            ],
            "specifications": [
                {"name": "Màn hình", "value": "TFT 1.6 inch"},
                {"name": "Pin", "value": "420mAh"},
                {"name": "Bluetooth", "value": "5.2"},
                {"name": "Chống nước", "value": "5ATM"},
            ],
        },
        {
            "product": {
                "name": "SmartWatch Mini",
                "subtitle": "Đồng hồ thông minh nhỏ gọn cho sử dụng hằng ngày",
                "description": "Thiết kế nhẹ, dễ đeo, phù hợp theo dõi sức khỏe cơ bản.",
                "price": 1990000,
                "image": "/images/watch-mini.png",
            },
            "features": [
                {
                    "title": "Sleep Tracking",
                    "description": "Theo dõi giấc ngủ và gợi ý cải thiện thói quen nghỉ ngơi.",
                    "icon": "moon",
                },
                {
                    "title": "Notification",
                    "description": "Nhận thông báo cuộc gọi, tin nhắn và ứng dụng.",
                    "icon": "bell",
                },
                {
                    "title": "Lightweight",
                    "description": "Thiết kế nhỏ gọn, thoải mái khi đeo cả ngày.",
                    "icon": "watch",
                },
            ],
            "specifications": [
                {"name": "Màn hình", "value": "AMOLED 1.4 inch"},
                {"name": "Pin", "value": "300mAh"},
                {"name": "Bluetooth", "value": "5.0"},
                {"name": "Chống nước", "value": "IP67"},
            ],
        },
    ]

    main_product = None

    for item in products:
        product_data = item["product"]
        product = Product.query.filter(Product.name == product_data["name"]).first()

        if product is None:
            product = Product(**product_data)
            db.session.add(product)
            db.session.flush()

            features = [
                Feature(product_id=product.id, **feature)
                for feature in item["features"]
            ]
            specifications = [
                Specification(product_id=product.id, **specification)
                for specification in item["specifications"]
            ]

            db.session.add_all(features)
            db.session.add_all(specifications)

        if product.name == "SmartWatch AI Pro":
            main_product = product

    return main_product


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
    create_sample_subscribers(product)
    create_sample_chat_history(product)


def init_db():
    with app.app_context():
        db.create_all()
        create_sample_data()
        db.session.commit()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
