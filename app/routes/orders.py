from flask import Blueprint, request
from app.extensions import db
from app.models.order import Order
from app.models.user import User
from app.services.order_service import OrderService
from app.utils.responses import success_response, error_response

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('', methods=['GET'])
def get_orders():
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return error_response("Missing user_id parameter", 400)
        
        user = User.query.get(user_id)
        if not user:
            return error_response("User not found", 404)
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = Order.query.filter_by(user_id=user.id)\
            .order_by(Order.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return success_response({
            'orders': [order.to_dict() for order in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        }, "Orders retrieved successfully")
        
    except Exception as e:
        return error_response(str(e), 500)


@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return error_response("Missing user_id parameter", 400)
        
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            return error_response("Order not found", 404)
        
        return success_response(order.to_dict(), "Order retrieved successfully")
        
    except Exception as e:
        return error_response(str(e), 500)


@orders_bp.route('', methods=['POST'])
def create_order():
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return error_response("Missing user_id parameter", 400)
        
        user = User.query.get(user_id)
        if not user:
            return error_response("User not found", 404)
        
        data = request.get_json()
        
        if not data or 'address_id' not in data:
            return error_response("Missing address_id")
        
        if not data or 'items' not in data or not data['items']:
            return error_response("Missing items")
        
        payment_method = data.get('payment_method', 'cash_on_delivery')
        notes = data.get('notes')
        
        order, error = OrderService.create_order(
            user,
            data['address_id'],
            payment_method,
            notes,
            data['items']
        )
        
        if error:
            return error_response(error, 400)
        
        return success_response(order.to_dict(), "Order created successfully", 201)
        
    except Exception as e:
        return error_response(str(e), 500)


@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return error_response("Missing user_id parameter", 400)
        
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            return error_response("Order not found", 404)
        
        success, error = OrderService.cancel_order(order)
        
        if error:
            return error_response(error, 400)
        
        return success_response(order.to_dict(), "Order cancelled successfully")
        
    except Exception as e:
        return error_response(str(e), 500)
