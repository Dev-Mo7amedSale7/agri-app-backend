from flask import Blueprint, request
from app.extensions import db
from app.models.user import User
from app.utils.responses import success_response, error_response

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['name', 'phone', 'password', 'confirm_password']):
            return error_response("Missing required fields")
        
        if data['password'] != data['confirm_password']:
            return error_response("Passwords do not match")
        
        # Check if phone already exists
        if User.query.filter_by(phone=data['phone']).first():
            return error_response("Phone number already registered")
        
        # Create new user
        user = User(
            name=data['name'],
            phone=data['phone']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return success_response({
            'user': user.to_dict()
        }, "Registration successful", 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['phone', 'password']):
            return error_response("Missing phone or password")
        
        user = User.query.filter_by(phone=data['phone']).first()
        
        if not user or not user.check_password(data['password']):
            return error_response("Invalid phone or password", 401)
        
        return success_response({
            'user': user.to_dict()
        }, "Login successful")
        
    except Exception as e:
        return error_response(str(e), 500)


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return error_response("Missing user_id parameter", 400)
        
        user = User.query.get(user_id)
        if not user:
            return error_response("User not found", 404)
        
        return success_response(user.to_dict(), "User retrieved successfully")
    except Exception as e:
        return error_response(str(e), 500)
