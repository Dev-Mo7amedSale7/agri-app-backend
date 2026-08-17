from flask import Blueprint, request
from app.extensions import db
from app.models.admin import Admin
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.services.product_service import ProductService
from app.services.order_service import OrderService
from app.utils.responses import success_response, error_response

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    def decorated_function(*args, **kwargs):
        admin_id = request.args.get('admin_id', type=int)
        if not admin_id:
            return error_response("Missing admin_id parameter", 400)
        
        admin = Admin.query.get(admin_id)
        if not admin:
            return error_response("Admin not found", 404)
        
        return f(admin, *args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@admin_bp.route('/login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['username', 'password']):
            return error_response("Missing username or password")
        
        admin = Admin.query.filter_by(username=data['username']).first()
        
        if not admin or not admin.check_password(data['password']):
            return error_response("Invalid username or password", 401)
        
        return success_response({
            'admin': admin.to_dict()
        }, "Admin login successful")
        
    except Exception as e:
        return error_response(str(e), 500)


# Product Routes
@admin_bp.route('/products', methods=['POST'])
@admin_required
def create_product(admin):
    try:
        data = request.get_json()
        
        required_fields = ['name', 'price', 'unit', 'category_id']
        if not data or not all(k in data for k in required_fields):
            return error_response("Missing required fields")
        
        product, error = ProductService.create_product(data)
        
        if error:
            return error_response(error, 400)
        
        return success_response(product.to_dict(), "Product created successfully", 201)
        
    except Exception as e:
        return error_response(str(e), 500)


@admin_bp.route('/products/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(admin, product_id):
    try:
        data = request.get_json()
        
        product, error = ProductService.update_product(product_id, data)
        
        if error:
            return error_response(error, 400)
        
        return success_response(product.to_dict(), "Product updated successfully")
        
    except Exception as e:
        return error_response(str(e), 500)


@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(admin, product_id):
    try:
        success, error = ProductService.delete_product(product_id)
        
        if error:
            return error_response(error, 400)
        
        return success_response(None, "Product deleted successfully")
        
    except Exception as e:
        return error_response(str(e), 500)


@admin_bp.route('/products/<int:product_id>/stock', methods=['PATCH'])
@admin_required
def update_product_stock(admin, product_id):
    try:
        data = request.get_json()
        
        if not data or 'quantity' not in data:
            return error_response("Missing quantity")
        
        product, error = ProductService.update_stock(product_id, data['quantity'])
        
        if error:
            return error_response(error, 400)
        
        return success_response(product.to_dict(), "Product stock updated successfully")
        
    except Exception as e:
        return error_response(str(e), 500)


@admin_bp.route('/products/<int:product_id>/availability', methods=['PATCH'])
@admin_required
def update_product_availability(admin, product_id):
    try:
        data = request.get_json()
        
        if not data or 'is_available' not in data:
            return error_response("Missing is_available")
        
        product, error = ProductService.update_availability(product_id, data['is_available'])
        
        if error:
            return error_response(error, 400)
        
        return success_response(product.to_dict(), "Product availability updated successfully")
        
    except Exception as e:
        return error_response(str(e), 500)


# Category Routes
@admin_bp.route('/categories', methods=['POST'])
@admin_required
def create_category(admin):
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return error_response("Missing name")
        
        category = Category(
            name=data['name'],
            image_url=data.get('image_url')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return success_response(category.to_dict(), "Category created successfully", 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


@admin_bp.route('/categories/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(admin, category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return error_response("Category not found", 404)
        
        data = request.get_json()
        
        if 'name' in data:
            category.name = data['name']
        if 'image_url' in data:
            category.image_url = data['image_url']
        
        db.session.commit()
        
        return success_response(category.to_dict(), "Category updated successfully")
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


@admin_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(admin, category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return error_response("Category not found", 404)
        
        db.session.delete(category)
        db.session.commit()
        
        return success_response(None, "Category deleted successfully")
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


# Order Routes
@admin_bp.route('/orders', methods=['GET'])
@admin_required
def get_all_orders(admin):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        query = Order.query
        
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.order_by(Order.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return success_response({
            'orders': [order.to_dict() for order in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        }, "Orders retrieved successfully")
        
    except Exception as e:
        return error_response(str(e), 500)


@admin_bp.route('/orders/<int:order_id>', methods=['GET'])
@admin_required
def get_order_detail(admin, order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return error_response("Order not found", 404)
        
        return success_response(order.to_dict(), "Order retrieved successfully")
        
    except Exception as e:
        return error_response(str(e), 500)


@admin_bp.route('/orders/<int:order_id>/status', methods=['PATCH'])
@admin_required
def update_order_status(admin, order_id):
    try:
        data = request.get_json()
        
        if not data or 'status' not in data:
            return error_response("Missing status")
        
        valid_statuses = ['pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled']
        if data['status'] not in valid_statuses:
            return error_response(f"Invalid status. Valid statuses: {', '.join(valid_statuses)}")
        
        order = Order.query.get(order_id)
        if not order:
            return error_response("Order not found", 404)
        
        success, error = OrderService.update_order_status(order, data['status'])
        
        if error:
            return error_response(error, 400)
        
        return success_response(order.to_dict(), "Order status updated successfully")
        
    except Exception as e:
        return error_response(str(e), 500)
