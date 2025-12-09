"""Routes cho admin - quản lý farmers và hệ thống"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import utils

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@utils.admin_required
def dashboard():
    """Trang dashboard admin - quản lý farmers"""
    users_data = utils.load_users()
    all_users = users_data.get('users', [])
    
    # Lọc chỉ farmers (không phải admin)
    farmers = [user for user in all_users if user.get('role') != 'admin']
    
    # Sắp xếp theo thời gian tạo
    farmers.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    # Lấy thông tin admin
    admin_info = utils.get_user_info(session)
    
    # Thống kê
    stats = {
        'total_farmers': len(farmers),
        'total_products': len(utils.load_data().get('products', []))
    }
    
    return render_template('admin/dashboard.html', farmers=farmers, admin=admin_info, stats=stats)

@admin_bp.route('/admin/farmers')
@utils.admin_required
def manage_farmers():
    """Trang quản lý farmers"""
    users_data = utils.load_users()
    all_users = users_data.get('users', [])
    
    # Lọc chỉ farmers
    farmers = [user for user in all_users if user.get('role') != 'admin']
    farmers.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    admin_info = utils.get_user_info(session)
    return render_template('admin/farmers.html', farmers=farmers, admin=admin_info)

@admin_bp.route('/admin/farmers/<username>/edit', methods=['GET', 'POST'])
@utils.admin_required
def edit_farmer(username):
    """Chỉnh sửa thông tin farmer"""
    users_data = utils.load_users()
    all_users = users_data.get('users', [])
    
    # Tìm farmer
    farmer = None
    farmer_index = -1
    for i, user in enumerate(all_users):
        if user.get('username') == username and user.get('role') != 'admin':
            farmer = user
            farmer_index = i
            break
    
    if not farmer:
        flash('Không tìm thấy farmer!', 'error')
        return redirect(url_for('admin.manage_farmers'))
    
    if request.method == 'POST':
        # Cập nhật thông tin
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        
        if not full_name:
            admin_info = utils.get_user_info(session)
            return render_template('admin/edit_farmer.html', farmer=farmer, admin=admin_info, error='Vui lòng điền họ và tên!')
        
        # Cập nhật
        farmer['full_name'] = full_name
        farmer['phone'] = phone
        farmer['email'] = email
        farmer['address'] = address
        farmer['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Lưu lại
        all_users[farmer_index] = farmer
        users_data['users'] = all_users
        utils.save_users(users_data)
        
        flash('Cập nhật thông tin farmer thành công!', 'success')
        return redirect(url_for('admin.manage_farmers'))
    
    admin_info = utils.get_user_info(session)
    return render_template('admin/edit_farmer.html', farmer=farmer, admin=admin_info)

@admin_bp.route('/admin/farmers/<username>/delete', methods=['POST'])
@utils.admin_required
def delete_farmer(username):
    """Xóa farmer"""
    # Không cho xóa chính mình
    if username == session.get('user_id'):
        flash('Không thể xóa chính mình!', 'error')
        return redirect(url_for('admin.manage_farmers'))
    
    users_data = utils.load_users()
    all_users = users_data.get('users', [])
    
    # Tìm và xóa farmer
    updated_users = []
    found = False
    for user in all_users:
        if user.get('username') == username:
            if user.get('role') == 'admin':
                flash('Không thể xóa admin!', 'error')
                return redirect(url_for('admin.manage_farmers'))
            found = True
        else:
            updated_users.append(user)
    
    if found:
        users_data['users'] = updated_users
        utils.save_users(users_data)
        flash('Xóa farmer thành công!', 'success')
    else:
        flash('Không tìm thấy farmer!', 'error')
    
    return redirect(url_for('admin.manage_farmers'))

@admin_bp.route('/admin/products')
@utils.admin_required
def manage_products():
    """Trang quản lý tất cả sản phẩm (admin xem được tất cả)"""
    data = utils.load_data()
    products = data.get('products', [])
    products.sort(key=lambda x: x.get('id', 0), reverse=True)
    
    admin_info = utils.get_user_info(session)
    return render_template('admin/products.html', products=products, admin=admin_info)

