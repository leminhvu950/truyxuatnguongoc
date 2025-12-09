"""Các hàm tiện ích"""
import json
import os
import hashlib
import time
import shutil
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps
from flask import redirect, url_for, request, session
import config

def init_directories():
    """Tạo các thư mục cần thiết nếu chưa tồn tại"""
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.QRCODE_DIR, exist_ok=True)
    os.makedirs(config.UPLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.join(config.UPLOAD_DIR, 'production'), exist_ok=True)
    os.makedirs(os.path.join(config.UPLOAD_DIR, 'harvest'), exist_ok=True)

def load_data():
    """Đọc dữ liệu từ data.json, tạo file mới nếu chưa có"""
    # Prefer ephemeral writable path (/tmp) on serverless if present
    tmp_data_file = os.path.join('/tmp', config.DATA_FILE)
    # If tmp file exists, prefer it
    if os.path.exists(tmp_data_file):
        try:
            with open(tmp_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi đọc tmp data file: {e}")

    if os.path.exists(config.DATA_FILE):
        try:
            with open(config.DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Lỗi đọc file JSON: {str(e)}")
            return {}
        except Exception as e:
            print(f"Lỗi không xác định khi đọc data.json: {str(e)}")
            return {}
    else:
        # Tạo file mới với cấu trúc rỗng (try to create in data dir, fallback to /tmp)
        try:
            save_data({})
            return {}
        except Exception:
            # fallback: write to tmp
            try:
                os.makedirs(os.path.dirname(tmp_data_file), exist_ok=True)
                with open(tmp_data_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=2)
                return {}
            except Exception as e:
                print(f"Failed to create data file in /tmp: {e}")
                return {}

def save_data(data):
    """Lưu dữ liệu vào data.json"""
    try:
        with open(config.DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return
    except Exception as e:
        print(f"Lỗi khi lưu data.json: {str(e)}")
        # fallback to /tmp
        try:
            tmp_path = os.path.join('/tmp', config.DATA_FILE)
            os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
            with open(tmp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Saved data.json to tmp: {tmp_path}")
            return
        except Exception as e2:
            print(f"Failed to save data.json to /tmp: {e2}")
            raise

def load_users():
    """Đọc dữ liệu user từ users.json"""
    tmp_users_file = os.path.join('/tmp', config.USERS_FILE)
    # If tmp users exists, prefer it
    if os.path.exists(tmp_users_file):
        try:
            with open(tmp_users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi đọc tmp users file: {e}")

    if os.path.exists(config.USERS_FILE):
        try:
            with open(config.USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Lỗi đọc file users.json: {str(e)}")
            return {}
        except Exception as e:
            print(f"Lỗi không xác định khi đọc users.json: {str(e)}")
            return {}
    else:
        # Tạo file mới với admin user mặc định
        default_users = {
            'users': [
                {
                    'username': 'admin',
                    'password': hash_password('admin123'),  # Mật khẩu: admin123
                    'full_name': 'Quản trị viên',
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ]
        }
        try:
            save_users(default_users)
            return default_users
        except Exception:
            # fallback: save to tmp
            try:
                os.makedirs(os.path.dirname(tmp_users_file), exist_ok=True)
                with open(tmp_users_file, 'w', encoding='utf-8') as f:
                    json.dump(default_users, f, ensure_ascii=False, indent=2)
                return default_users
            except Exception as e:
                print(f"Failed to create tmp users file: {e}")
                return default_users

def save_users(users_data):
    """Lưu dữ liệu user vào users.json"""
    try:
        with open(config.USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
        return
    except Exception as e:
        print(f"Lỗi khi lưu users.json: {str(e)}")
        # fallback to /tmp
        try:
            tmp_path = os.path.join('/tmp', config.USERS_FILE)
            os.makedirs(os.path.dirname(tmp_path), exist_ok=True)
            with open(tmp_path, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, ensure_ascii=False, indent=2)
            print(f"Saved users.json to tmp: {tmp_path}")
            return
        except Exception as e2:
            print(f"Failed to save users.json to /tmp: {e2}")
            raise

def hash_password(password):
    """Mã hóa mật khẩu bằng bcrypt (an toàn)"""
    try:
        import bcrypt
        # Tạo salt và hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    except Exception:
        # Nếu bcrypt không khả dụng, fallback sang Werkzeug's generate_password_hash
        try:
            from werkzeug.security import generate_password_hash
            return generate_password_hash(password)
        except Exception:
            # Cuối cùng fallback sang MD5 (không khuyến nghị) — đảm bảo không crash
            return hashlib.md5(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Xác thực mật khẩu"""
    # Nếu hash là dạng Werkzeug (ví dụ 'pbkdf2:sha256:...'), dùng check_password_hash
    try:
        from werkzeug.security import check_password_hash
        # Werkzeug hashes are strings that contain ':' as algorithm marker
        if isinstance(hashed, str) and (hashed.startswith('pbkdf2:') or ':' in hashed):
            return check_password_hash(hashed, password)
    except Exception:
        pass

    # Thử bcrypt nếu có
    try:
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        # Fallback cho mật khẩu cũ dùng MD5 (migration)
        try:
            old_hash = hashlib.md5(password.encode()).hexdigest()
            return old_hash == hashed
        except Exception:
            return False

def login_required(f):
    """Decorator để yêu cầu đăng nhập"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """Kiểm tra extension file có được phép không"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def is_image_file(filename):
    """Kiểm tra file có phải là hình ảnh không"""
    image_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in image_extensions

def is_video_file(filename):
    """Kiểm tra file có phải là video không"""
    video_extensions = {'mp4', 'mov', 'avi', 'mkv', 'webm'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in video_extensions

def save_uploaded_files(files, product_id, upload_type):
    """Lưu các file đã upload và trả về danh sách đường dẫn"""
    saved_files = []
    if not files:
        return saved_files

    upload_folder = os.path.join(config.UPLOAD_DIR, upload_type, product_id)
    os.makedirs(upload_folder, exist_ok=True)

    for file in files:
        if file and file.filename and allowed_file(file.filename):
            # Kiểm tra kích thước file
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)  # Reset về đầu file

            if file_size > config.MAX_FILE_SIZE:
                print(f"File {file.filename} quá lớn ({file_size} bytes, tối đa {config.MAX_FILE_SIZE} bytes)")
                continue

            if file_size == 0:
                print(f"File {file.filename} rỗng")
                continue

            # Tạo tên file an toàn
            filename = secure_filename(file.filename)
            # Thêm timestamp để tránh trùng tên
            timestamp = str(int(time.time() * 1000))
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{timestamp}{ext}"
            file_path = os.path.join(upload_folder, new_filename)

            try:
                file.save(file_path)
                # Lưu đường dẫn tương đối để hiển thị
                relative_path = f"uploads/{upload_type}/{product_id}/{new_filename}"
                saved_files.append(relative_path)
            except Exception as e:
                print(f"Lỗi khi lưu file {filename}: {str(e)}")
                continue

    return saved_files

def generate_qrcode(product_id, base_url):
    """Tạo mã QR cho sản phẩm"""
    import qrcode

    # URL của trang sản phẩm (loại bỏ dấu / cuối nếu có)
    base = base_url.rstrip('/')
    url = f"{base}/product/{product_id}"

    # Tạo QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Tạo hình ảnh QR
    img = qr.make_image(fill_color="black", back_color="white")

    # Lưu vào thư mục static/qrcodes
    qr_path = os.path.join(config.QRCODE_DIR, f'{product_id}.png')
    img.save(qr_path)

    return qr_path

def delete_product_files(product_id):
    """Xóa tất cả file liên quan đến sản phẩm (QR code và media)"""
    # Xóa file QR code
    qr_path = os.path.join(config.QRCODE_DIR, f'{product_id}.png')
    if os.path.exists(qr_path):
        try:
            os.remove(qr_path)
        except:
            pass

    # Xóa thư mục media của sản phẩm
    production_media_dir = os.path.join(config.UPLOAD_DIR, 'production', product_id)
    harvest_media_dir = os.path.join(config.UPLOAD_DIR, 'harvest', product_id)

    for media_dir in [production_media_dir, harvest_media_dir]:
        if os.path.exists(media_dir):
            try:
                shutil.rmtree(media_dir)
            except:
                pass

def get_user_info(session):
    """Lấy thông tin user từ session"""
    if 'user_id' not in session:
        return None

    users_data = load_users()
    for user in users_data.get('users', []):
        if user.get('username') == session.get('user_id'):
            return {
                'username': user.get('username'),
                'full_name': user.get('full_name', user.get('username'))
            }
    return None

