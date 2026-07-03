from backend.models import Feature, Product, Specification


def get_product():
    return Product.query.first()


def get_features():
    return Feature.query.all()


def get_specifications():
    return Specification.query.all()


def get_product_detail():
    product = get_product()

    if product is None:
        return None

    return {
        "id": product.id,
        "name": product.name,
        "subtitle": product.subtitle,
        "description": product.description,
        "price": format_price(product.price),
        "image": product.image,
        "image_url": product.image,
        "features": [feature_to_dict(f) for f in product.features],
        "specifications": [specification_to_dict(s) for s in product.specifications],
    }


def feature_to_dict(feature):
    return {
        "id": feature.id,
        "title": feature.title,
        "description": feature.description,
        "icon": feature.icon,
    }


def specification_to_dict(specification):
    return {
        "id": specification.id,
        "name": specification.name,
        "value": specification.value,
    }


def format_price(price):
    if price is None:
        return None

    return f"{int(price):,}".replace(",", ".") + "đ"
