"""Routes cho admin - quản lý hệ thống"""
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import utils

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator yêu cầu quyền admin"""
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login', next=request.url))
        
        # Kiểm tra role admin
        users_data = utils.load_users()
        current_user = None
        for user in users_data.get('users', []):
            if user.get('username') == session.get('user_id'):
                current_user = user
                break
        
        if not current_user or current_user.get('role') != 'admin':
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    """Trang dashboard admin"""
    data = utils.load_data()
    users_data = utils.load_users()
    
    # Thống kê
    stats = {
        'total_products': len(data.get('products', [])),
        'total_farmers': len([u for u in users_data.get('users', []) if u.get('role') != 'admin']),
        'total_scans': sum(p.get('scan_count', 0) for p in data.get('products', [])),
        'recent_products': sorted(data.get('products', []), key=lambda x: x.get('created_at', ''), reverse=True)[:5]
    }
    
    # Lấy thông tin admin
    admin_info = utils.get_user_info(session)
    
    return render_template('admin/dashboard.html', stats=stats, user=admin_info)

@admin_bp.route('/farmers')
@admin_required
def manage_farmers():
    """Quản lý farmers"""
    users_data = utils.load_users()
    farmers = [u for u in users_data.get('users', []) if u.get('role') != 'admin']
    
    # Thống kê sản phẩm cho mỗi farmer
    data = utils.load_data()
    products = data.get('products', [])
    
    for farmer in farmers:
        farmer_products = [p for p in products if p.get('created_by') == farmer.get('username')]
        farmer['product_count'] = len(farmer_products)
        farmer['total_scans'] = sum(p.get('scan_count', 0) for p in farmer_products)
    
    admin_info = utils.get_user_info(session)
    return render_template('admin/farmers.html', farmers=farmers, user=admin_info)

@admin_bp.route('/products')
@admin_required
def manage_products():
    """Quản lý tất cả sản phẩm"""
    data = utils.load_data()
    products = data.get('products', [])
    
    # Sắp xếp theo thời gian tạo mới nhất
    products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    # Lấy thông tin farmer cho mỗi sản phẩm
    users_data = utils.load_users()
    user_map = {u.get('username'): u for u in users_data.get('users', [])}
    
    for product in products:
        created_by = product.get('created_by')
        if created_by and created_by in user_map:
            product['farmer_info'] = user_map[created_by]
    
    admin_info = utils.get_user_info(session)
    return render_template('admin/products.html', products=products, user=admin_info)

@admin_bp.route('/farmer/<username>')
@admin_required
def farmer_detail(username):
    """Chi tiết farmer và sản phẩm của họ"""
    users_data = utils.load_users()
    farmer = None
    
    for user in users_data.get('users', []):
        if user.get('username') == username and user.get('role') != 'admin':
            farmer = user
            break
    
    if not farmer:
        return redirect(url_for('admin.manage_farmers'))
    
    # Lấy sản phẩm của farmer
    data = utils.load_data()
    farmer_products = [p for p in data.get('products', []) if p.get('created_by') == username]
    farmer_products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    admin_info = utils.get_user_info(session)
    return render_template('admin/farmer_detail.html', farmer=farmer, products=farmer_products, user=admin_info)

@admin_bp.route('/delete_farmer/<username>', methods=['POST'])
@admin_required
def delete_farmer(username):
    """Xóa farmer (chỉ admin)"""
    if username == 'admin':
        return jsonify({'success': False, 'message': 'Không thể xóa tài khoản admin!'})
    
    users_data = utils.load_users()
    users = users_data.get('users', [])
    
    # Tìm và xóa user
    for i, user in enumerate(users):
        if user.get('username') == username:
            users.pop(i)
            break
    
    # Lưu lại
    users_data['users'] = users
    utils.save_users(users_data)
    
    # Xóa tất cả sản phẩm của farmer này
    data = utils.load_data()
    products = data.get('products', [])
    farmer_products = [p for p in products if p.get('created_by') == username]
    
    # Xóa files của các sản phẩm
    for product in farmer_products:
        utils.delete_product_files(product.get('id'))
    
    # Xóa sản phẩm khỏi database
    data['products'] = [p for p in products if p.get('created_by') != username]
    utils.save_data(data)
    
    return jsonify({'success': True, 'message': 'Đã xóa farmer và tất cả sản phẩm!'})

@admin_bp.route('/delete_product/<product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    """Xóa sản phẩm (admin có thể xóa bất kỳ sản phẩm nào)"""
    data = utils.load_data()
    products = data.get('products', [])
    
    # Tìm và xóa sản phẩm
    product_found = False
    for i, p in enumerate(products):
        if p.get('id') == product_id:
            products.pop(i)
            product_found = True
            break
    
    if product_found:
        data['products'] = products
        utils.save_data(data)
        
        # Xóa file QR code và media
        utils.delete_product_files(product_id)
        
        return jsonify({'success': True, 'message': 'Đã xóa sản phẩm!'})
    
    return jsonify({'success': False, 'message': 'Không tìm thấy sản phẩm!'})

@admin_bp.route('/toggle_farmer_status/<username>', methods=['POST'])
@admin_required
def toggle_farmer_status(username):
    """Kích hoạt/vô hiệu hóa farmer"""
    users_data = utils.load_users()
    users = users_data.get('users', [])
    
    for user in users:
        if user.get('username') == username:
            current_status = user.get('status', 'active')
            user['status'] = 'inactive' if current_status == 'active' else 'active'
            user['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            break
    
    utils.save_users(users_data)
    
    return jsonify({'success': True, 'message': 'Đã cập nhật trạng thái farmer!'})