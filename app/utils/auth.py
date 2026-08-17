from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User
from app.models.admin import Admin


def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(int(user_id))
            if not user:
                return jsonify({'success': False, 'message': 'User not found', 'data': None}), 404
            return f(user, *args, **kwargs)
        except Exception as e:
            return jsonify({'success': False, 'message': str(e), 'data': None}), 401
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            admin_id = get_jwt_identity()
            admin = Admin.query.get(int(admin_id))
            if not admin:
                return jsonify({'success': False, 'message': 'Admin not found', 'data': None}), 404
            return f(admin, *args, **kwargs)
        except Exception as e:
            return jsonify({'success': False, 'message': str(e), 'data': None}), 401
    return decorated_function
