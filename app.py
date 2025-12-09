"""Flask Application - Truy xuất nguồn gốc nông sản"""
from flask import Flask
from flask_wtf.csrf import CSRFProtect
import os
import config
import utils
from routes.main import main_bp
from routes.auth import auth_bp
from routes.products import products_bp
from routes.admin import admin_bp
import traceback
import logging

app = Flask(__name__)
# Cấu hình ứng dụng
app.config.from_object(config)
app.secret_key = config.SECRET_KEY

# Bảo vệ CSRF
csrf = CSRFProtect(app)

# Đăng ký blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(admin_bp)

# Khởi tạo thư mục và dữ liệu sẽ thực hiện khi function được gọi (lazy init)
def _initialize_app():
    try:
        utils.init_directories()
    except Exception as e:
        print(f"Warning: failed to init directories: {e}")
    try:
        utils.load_data()
    except Exception as e:
        print(f"Warning: failed to load data: {e}")
    try:
        utils.load_users()
    except Exception as e:
        print(f"Warning: failed to load users: {e}")


# Fallback for Flask versions without `before_first_request`: run init once on first request
_initialized = False

@app.before_request
def _maybe_initialize():
    global _initialized
    if not _initialized:
        _initialize_app()
        _initialized = True


# Global exception handler to ensure traceback is printed to logs
def _setup_global_error_logging(app):
    # ensure logger prints to stdout
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    @app.errorhandler(Exception)
    def _handle_unhandled_exception(e):
        # log exception with stack trace
        app.logger.exception('Unhandled exception: %s', e)
        try:
            traceback.print_exc()
        except Exception:
            pass
        # Return generic error to user
        return 'Internal Server Error', 500


_setup_global_error_logging(app)


if __name__ == '__main__':
    # Chỉ chạy debug mode khi chạy local
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

