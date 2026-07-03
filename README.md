# SmartWatch AI Pro Website

Landing page giới thiệu sản phẩm SmartWatch AI Pro, xây dựng theo đề bài vòng 2 TTS IT phát triển website của Helicorp.

## Demo

- Frontend: https://smartwatch-ai-pro-website.pages.dev/

## Tính năng chính

- Landing page responsive gồm Hero, tính năng nổi bật, thông số kỹ thuật và form đăng ký nhận tin.
- Dữ liệu sản phẩm, ảnh, tính năng và thông số được lấy từ backend/database.
- Form đăng ký nhận tin có validate phía frontend và lưu subscriber vào database.
- Chatbot tư vấn sản phẩm dạng cửa sổ nổi ở góc màn hình.
- Dark mode / light mode.
- Scroll reveal animation, micro-interactions và tối ưu ảnh hero cho PageSpeed.
- SEO meta cơ bản: title, description, Open Graph, Twitter card.

## Công nghệ sử dụng

Frontend:

- React
- React Bootstrap
- Axios
- CSS custom
- Cloudflare Pages

Backend:

- Flask
- Flask-CORS
- Flask-SQLAlchemy
- PyMySQL
- Gunicorn
- MySQL/Aiven MySQL

AI chatbot:

- Hỗ trợ OpenAI hoặc Gemini qua biến môi trường.
- Có fallback rule-based nếu không cấu hình API key.

## Cấu trúc thư mục

```text
.
├── backend/
│   ├── app.py
│   ├── __init__.py
│   ├── init_db.py
│   ├── models.py
│   ├── dao/
│   ├── routes/
│   └── utils/
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── .env.example
├── docs/
├── Procfile
├── requirements.txt
└── .env.example
```

## Cài đặt backend

Tạo môi trường ảo và cài dependency:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend\requirements.txt
```

Tạo file `.env` ở thư mục gốc dự án dựa trên `.env.example`:

```env
SECRET_KEY=change-this-secret-key

AIVEN_DB_HOST=your-aiven-mysql-host.aivencloud.com
AIVEN_DB_PORT=12345
AIVEN_DB_USER=avnadmin
AIVEN_DB_PASSWORD=your-aiven-password
AIVEN_DB_NAME=smartwatch_ai_pro
AIVEN_DB_SSL_CA=

GEMINI_API_KEY=
GEMINI_MODEL=gemini-flash-latest
GEMINI_ENABLE_MODEL_FALLBACK=false
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
AI_TIMEOUT_SECONDS=8
CHATBOT_PRODUCT_CACHE_SECONDS=300
```

Khởi tạo bảng và dữ liệu mẫu:

```powershell
.\.venv\Scripts\python.exe backend\init_db.py
```

Chạy backend local:

```powershell
.\.venv\Scripts\python.exe backend\app.py
```

Backend mặc định chạy tại:

```text
http://localhost:5000/api
```

## Cài đặt frontend

```powershell
cd frontend
npm install
```

Tạo file `frontend/.env` dựa trên `frontend/.env.example`:

```env
REACT_APP_API_BASE_URL=http://localhost:5000/api
```

Chạy frontend local:

```powershell
npm start
```

Frontend mặc định chạy tại:

```text
http://localhost:3000
```

Build production:

```powershell
npm run build
```

Nếu PowerShell chặn `npm.ps1`, dùng:

```powershell
npm.cmd run build
```

## API chính

Product:

```http
GET /api/product
```

Subscriber:

```http
POST /api/subscribers
GET /api/subscribers
```

Chatbot:

```http
POST /api/chat
GET /api/chat/history
```

## Dữ liệu mẫu

`backend/init_db.py` tạo:

- Product SmartWatch AI Pro.
- Features.
- Specifications.
- Subscriber mẫu.
- Chat history mẫu.

Hero chips lấy từ bảng `specification`, gồm:

- `Health Score`: `98%`
- `Battery`: `500mAh`

Ảnh sản phẩm được lưu trong cột `product.image` và frontend render trực tiếp từ URL database.

## Deploy

Frontend đã deploy trên Cloudflare Pages:

```text
https://smartwatch-ai-pro-website.pages.dev/
```

Backend có thể deploy lên Render/Railway/Fly.io hoặc nền tảng hỗ trợ Flask bằng `Procfile`:

```text
web: gunicorn backend.app:app --bind 0.0.0.0:$PORT
```

Khi deploy frontend, cấu hình biến môi trường:

```env
REACT_APP_API_BASE_URL=https://your-backend-domain/api
```

## Đối chiếu yêu cầu đề bài

Đã làm:

- Hero section.
- Section tính năng nổi bật.
- Section thông số kỹ thuật.
- Form đăng ký nhận tin.
- Responsive desktop/mobile.
- SEO meta cơ bản.
- Backend lưu trữ dữ liệu.
- Dark mode.
- Scroll animation.
- Chatbot góc màn hình.
- Tối ưu ảnh hero qua Cloudinary transform.

Cần bổ sung khi nộp:

- Link GitHub repository public.
- Link backend deploy nếu có.
- Ảnh chụp điểm Google PageSpeed Insights.
- Minh chứng các phần điểm cộng đã làm.

## Ghi chú

- Frontend không dùng ảnh mặc định local cho product; ảnh sản phẩm lấy từ database/API.
- Nếu trang local báo chưa tải được dữ liệu sản phẩm, kiểm tra backend đã chạy tại `http://localhost:5000/api` và database đã được init chưa.
