# Hệ thống Truy xuất Nguồn gốc Nông sản

Ứng dụng web Flask để quản lý và truy xuất nguồn gốc nông sản với mã QR.

## Tính năng

- ✅ Đăng ký/Đăng nhập người dùng
- ✅ Tạo và quản lý sản phẩm nông sản
- ✅ Tạo mã QR cho từng sản phẩm
- ✅ Upload hình ảnh/video sản xuất và thu hoạch
- ✅ Phân tích AI cơ bản cho báo cáo sản phẩm
- ✅ **AI nâng cao với OpenAI** - Phân tích chi tiết và gợi ý tiêu chuẩn số hóa
- ✅ **Admin Panel** - Quản lý người dùng và hệ thống
- ✅ **Hướng dẫn tiêu chuẩn số hóa** - Tài liệu chi tiết
- ✅ Responsive design

## Admin Panel

### Tính năng Admin:
- 📊 Dashboard với thống kê tổng quan
- 👥 Quản lý người dùng (tạo, sửa, xóa)
- 📦 Quản lý tất cả sản phẩm
- 🔧 Thông tin hệ thống
- 🛡️ Phân quyền admin/user

### Tài khoản Admin mặc định:
- **Username:** `admin`
- **Password:** `admin123`

> ⚠️ **Quan trọng:** Hãy đổi mật khẩu admin ngay sau khi deploy!

## AI nâng cao với OpenAI

### Tính năng AI:
- 🧠 **Phân tích sản phẩm chi tiết** - Đánh giá chất lượng thông tin và gợi ý cải thiện
- 📊 **Gợi ý tiêu chuẩn số hóa** - Hướng dẫn cụ thể để đạt tiêu chuẩn cao
- 📈 **Phân tích thị trường** - Dự đoán giá cả, xu hướng và cơ hội kinh doanh
- 📋 **Kế hoạch cải thiện** - Lộ trình cụ thể để nâng cao chất lượng sản phẩm
- 🎯 **Tư vấn marketing** - Chiến lược quảng bá và xây dựng thương hiệu

### Cấu hình OpenAI:
1. **Lấy API Key:**
   - Truy cập [platform.openai.com](https://platform.openai.com)
   - Tạo API key mới
   
2. **Cấu hình:**
   ```bash
   # Trong file .env hoặc biến môi trường
   OPENAI_API_KEY=sk-your-api-key-here
   OPENAI_MODEL=gpt-3.5-turbo  # hoặc gpt-4
   ```

3. **Sử dụng:**
   - Truy cập trang sản phẩm
   - Click "🤖 AI Analysis" để xem phân tích nâng cao
   - Xem gợi ý tiêu chuẩn số hóa và kế hoạch cải thiện

> **Lưu ý:** Tính năng AI nâng cao là tùy chọn. Nếu không cấu hình OpenAI API, hệ thống sẽ sử dụng phân tích AI cơ bản.

## Deploy lên Railway

### 1. Chuẩn bị
```bash
# Clone repository
git clone <your-repo-url>
cd khkt

# Cài đặt dependencies (optional - để test local)
pip install -r requirements.txt
```

### 2. Deploy trên Railway

1. **Tạo tài khoản Railway:**
   - Truy cập [railway.app](https://railway.app)
   - Đăng ký/Đăng nhập

2. **Tạo project mới:**
   - Click "New Project"
   - Chọn "Deploy from GitHub repo"
   - Kết nối với repository của bạn

3. **Cấu hình biến môi trường:**
   - Vào Settings > Variables
   - Thêm các biến sau:
   ```
   SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
   FLASK_ENV=production
   OPENAI_API_KEY=sk-your-openai-api-key-here (Tùy chọn - cho tính năng AI nâng cao)
   ```

4. **Deploy:**
   - Railway sẽ tự động detect Flask app
   - Build và deploy sẽ diễn ra tự động
   - Ứng dụng sẽ có URL dạng: `https://your-app.railway.app`

### 3. Sau khi deploy

1. **Đổi mật khẩu admin:**
   - Truy cập `/admin`
   - Đăng nhập với `admin/admin123`
   - Vào "Quản lý Users" > Edit admin > Đổi mật khẩu

2. **Tạo user mới:**
   - Sử dụng Admin Panel để tạo user
   - Hoặc cho phép user tự đăng ký

## Cấu trúc Project

```
khkt/
├── app.py              # Main Flask application
├── config.py           # Configuration
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
├── Procfile           # Railway deployment config
├── railway.json       # Railway settings
├── runtime.txt        # Python version
├── routes/            # Route blueprints
│   ├── main.py        # Main routes
│   ├── auth.py        # Authentication
│   ├── products.py    # Product management
│   └── admin.py       # Admin panel
├── templates/         # HTML templates
│   ├── admin/         # Admin templates
│   └── ...
├── static/            # Static files
│   ├── style.css
│   ├── qrcodes/       # Generated QR codes
│   └── uploads/       # User uploads
└── data/              # JSON data files
    ├── data.json      # Products data
    └── users.json     # Users data
```

## API Endpoints

### Public
- `GET /` - Trang chủ
- `GET /product/<id>` - Xem sản phẩm

### Authentication
- `GET/POST /login` - Đăng nhập
- `GET/POST /register` - Đăng ký
- `GET /logout` - Đăng xuất

### Products (User)
- `GET/POST /create` - Tạo sản phẩm
- `GET /manage` - Quản lý sản phẩm của user
- `GET/POST /edit/<id>` - Chỉnh sửa sản phẩm

### Admin Panel
- `GET /admin/` - Dashboard
- `GET /admin/users` - Quản lý users
- `GET/POST /admin/users/create` - Tạo user
- `GET/POST /admin/users/<username>/edit` - Sửa user
- `POST /admin/users/<username>/delete` - Xóa user
- `GET /admin/products` - Quản lý sản phẩm
- `POST /admin/products/<id>/delete` - Xóa sản phẩm
- `GET /admin/system` - Thông tin hệ thống

## Bảo mật

- ✅ CSRF Protection
- ✅ Password hashing với bcrypt
- ✅ Session management
- ✅ File upload validation
- ✅ Admin role-based access control

## Môi trường Development

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy development server
python app.py

# Truy cập: http://localhost:5000
```

## Troubleshooting

### Lỗi thường gặp:

1. **"No module named 'bcrypt'"**
   ```bash
   pip install bcrypt
   ```

2. **"Permission denied" khi upload file**
   - Kiểm tra quyền thư mục `static/uploads/`

3. **Admin không thể truy cập**
   - Kiểm tra role trong `data/users.json`
   - Đảm bảo user có `"role": "admin"`

## License

MIT License - Xem file LICENSE để biết thêm chi tiết.