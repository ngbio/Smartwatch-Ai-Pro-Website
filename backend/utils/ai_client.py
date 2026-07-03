import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from sqlalchemy.exc import SQLAlchemyError

from backend.dao import product_dao


PRODUCT_CACHE_TTL_SECONDS = int(os.environ.get("CHATBOT_PRODUCT_CACHE_SECONDS", "300"))
AI_TIMEOUT_SECONDS = int(os.environ.get("AI_TIMEOUT_SECONDS", "8"))

_product_cache = {
    "expires_at": 0,
    "data": None,
}

FALLBACK_PRODUCT = {
    "name": "SmartWatch AI Pro",
    "subtitle": "Đồng hồ AI chăm sóc sức khỏe thông minh",
    "description": "Theo dõi sức khỏe, luyện tập và giấc ngủ bằng AI.",
    "price": "3.990.000đ",
    "features": [
        {
            "title": "AI Health Tracking",
            "description": "Theo dõi sức khỏe bằng AI theo thời gian thực.",
        },
        {
            "title": "GPS",
            "description": "Định vị chính xác khi chạy bộ, đạp xe và luyện tập ngoài trời.",
        },
        {
            "title": "Fast Charging",
            "description": "Sạc nhanh, phù hợp với lịch trình bận rộn hằng ngày.",
        },
        {
            "title": "Waterproof",
            "description": "Chống nước chuẩn IP68 cho nhu cầu sinh hoạt hằng ngày.",
        },
    ],
    "specifications": [
        {"name": "Màn hình", "value": "AMOLED 1.8 inch"},
        {"name": "Pin", "value": "500mAh"},
        {"name": "Bluetooth", "value": "5.3"},
        {"name": "Chống nước", "value": "IP68"},
    ],
}


def generate_reply(message):
    prompt = build_prompt(message)

    if os.environ.get("GEMINI_API_KEY"):
        return call_gemini_api(prompt, message)

    if os.environ.get("OPENAI_API_KEY"):
        return call_openai_api(prompt, message)

    return get_default_reply(message)


def get_product_detail_safe():
    now = time.time()

    if _product_cache["data"] and _product_cache["expires_at"] > now:
        return _product_cache["data"]

    try:
        product = product_dao.get_product_detail() or FALLBACK_PRODUCT
    except SQLAlchemyError as ex:
        print(f"Database error while loading product for chatbot: {ex}")
        product = FALLBACK_PRODUCT

    _product_cache["data"] = product
    _product_cache["expires_at"] = now + PRODUCT_CACHE_TTL_SECONDS

    return product


def build_prompt(message):
    product = get_product_detail_safe()

    features = "\n".join(
        [f"- {f['title']}: {f['description']}" for f in product["features"]]
    )
    specifications = "\n".join(
        [f"- {s['name']}: {s['value']}" for s in product["specifications"]]
    )
    product_info = f"""
Tên sản phẩm: {product["name"]}
Mô tả ngắn: {product["subtitle"]}
Mô tả: {product["description"]}
Giá: {product["price"]}
Tính năng:
{features}
Thông số kỹ thuật:
{specifications}
"""

    return f"""
Bạn là nhân viên tư vấn của SmartWatch AI Pro.

Chỉ trả lời các câu hỏi liên quan đến:
- Tính năng
- Thông số kỹ thuật
- Giá
- Bảo hành

Nếu người dùng hỏi ngoài phạm vi sản phẩm thì lịch sự từ chối.
Trả lời ngắn gọn, rõ ràng, ưu tiên tiếng Việt tự nhiên.

Thông tin sản phẩm:
{product_info}

Câu hỏi của khách hàng:
{message}
"""


def call_gemini_api(prompt, fallback_message):
    api_key = os.environ.get("GEMINI_API_KEY")
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt,
                    }
                ]
            }
        ]
    }

    for index, model in enumerate(get_gemini_models()):
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={api_key}"
        )

        try:
            response = send_json_request(url, data)
            return response["candidates"][0]["content"]["parts"][0]["text"]
        except HTTPError as ex:
            if should_retry_gemini_model(ex, index):
                continue

            log_ai_error("Gemini", ex)
            return get_default_reply(fallback_message)
        except (URLError, KeyError, IndexError, TimeoutError) as ex:
            log_ai_error("Gemini", ex)
            return get_default_reply(fallback_message)

    return get_default_reply(fallback_message)


def should_retry_gemini_model(error, index):
    return (
        os.environ.get("GEMINI_ENABLE_MODEL_FALLBACK", "false").lower() == "true"
        and error.code == 404
        and index < len(get_gemini_models()) - 1
    )


def get_gemini_models():
    configured_model = os.environ.get("GEMINI_MODEL", "gemini-flash-latest").strip()

    if os.environ.get("GEMINI_ENABLE_MODEL_FALLBACK", "false").lower() != "true":
        return [configured_model]

    fallback_models = ["gemini-flash-latest", "gemini-2.5-flash"]
    models = [configured_model, *fallback_models]

    return list(dict.fromkeys([model for model in models if model]))


def call_openai_api(prompt, fallback_message):
    api_key = os.environ.get("OPENAI_API_KEY")
    url = "https://api.openai.com/v1/chat/completions"
    data = {
        "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    try:
        response = send_json_request(url, data, headers)
        return response["choices"][0]["message"]["content"]
    except (HTTPError, URLError, KeyError, IndexError, TimeoutError) as ex:
        log_ai_error("OpenAI", ex)
        return get_default_reply(fallback_message)


def send_json_request(url, data, headers=None):
    request_headers = {
        "Content-Type": "application/json",
    }

    if headers:
        request_headers.update(headers)

    request = Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=request_headers,
        method="POST",
    )

    with urlopen(request, timeout=AI_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def log_ai_error(provider, error):
    if isinstance(error, HTTPError):
        try:
            detail = error.read().decode("utf-8")
        except Exception:
            detail = str(error)

        print(f"{provider} API error {error.code}: {detail}")
        return

    print(f"{provider} API error: {error}")


def get_default_reply(message):
    product = get_product_detail_safe()
    text = message.lower()

    if "gia" in text or "giá" in text or "bao nhiêu" in text or "bao nhieu" in text:
        return f"{product['name']} hiện có giá {product['price']}."

    if "chống nước" in text or "chong nuoc" in text or "nước" in text or "nuoc" in text:
        return (
            "SmartWatch AI Pro có khả năng chống nước chuẩn IP68 cho nhu cầu sinh hoạt hằng ngày. "
            "Bạn nên hạn chế dùng trong môi trường áp lực nước cao hoặc nước nóng."
        )

    if "pin" in text or "sạc" in text or "sac" in text:
        return (
            "SmartWatch AI Pro dùng pin 500mAh và hỗ trợ sạc nhanh, phù hợp cho nhu cầu theo dõi "
            "sức khỏe, luyện tập và sử dụng hằng ngày."
        )

    if "gps" in text or "định vị" in text or "dinh vi" in text:
        return "Sản phẩm có GPS để định vị khi chạy bộ, đạp xe và luyện tập ngoài trời."

    if "bảo hành" in text or "bao hanh" in text:
        return (
            "SmartWatch AI Pro có chính sách bảo hành theo thông tin bán hàng của cửa hàng. "
            "Bạn có thể để lại thông tin để được tư vấn chi tiết hơn."
        )

    return (
        "Mình có thể tư vấn về tính năng, thông số kỹ thuật, giá và bảo hành "
        "của SmartWatch AI Pro."
    )
