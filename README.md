# Hệ thống Truy xuất Nguồn gốc Nông sản

Ứng dụng Flask để quản lý và truy xuất nguồn gốc nông sản thông qua mã QR.

## Tính năng

- 🔐 Đăng ký/Đăng nhập người dùng
- 📦 Tạo và quản lý sản phẩm nông sản
- 📱 Tạo mã QR cho từng sản phẩm
- 📸 Upload hình ảnh quá trình sản xuất và thu hoạch
- 🔍 Tìm kiếm sản phẩm
- 🤖 Phân tích AI (tùy chọn)

## Deploy lên Railway

### Bước 1: Chuẩn bị GitHub Repository

1. Tạo repository mới trên GitHub: `leminhvu950/truyxuatnguongoc`
2. Clone repository về máy hoặc push code hiện tại lên

### Bước 2: Deploy lên Railway

1. Truy cập [railway.app](https://railway.app)
2. Đăng nhập bằng GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Chọn repository `leminhvu950/truyxuatnguongoc`
5. Railway sẽ tự động detect Flask app và deploy

### Bước 3: Cấu hình Environment Variables (Tùy chọn)

Trong Railway dashboard:
- `SECRET_KEY`: Railway sẽ tự động generate
- Các biến khác nếu cần

## Chạy Local

```bash
pip install -r requirements.txt
python app.py
```

## Cấu trúc Project

```
├── app.py              # Main Flask application
├── config.py           # Configuration
├── utils.py            # Utility functions
├── ai_analysis.py      # AI analysis module
├── routes/             # Route blueprints
├── templates/          # HTML templates
├── static/             # Static files (CSS, uploads, QR codes)
├── data/               # JSON database files
├── requirements.txt    # Python dependencies
├── railway.toml        # Railway configuration
└── Procfile           # Process configuration
```