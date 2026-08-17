from flask import Blueprint, request
from app.extensions import db
from app.models.address import Address
from app.utils.responses import success_response, error_response

addresses_bp = Blueprint('addresses', __name__)


@addresses_bp.route('', methods=['GET'])
def get_addresses():
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return error_response("Missing user_id parameter", 400)
        
        addresses = Address.query.filter_by(user_id=user_id).all()
        return success_response(
            [address.to_dict() for address in addresses],
            "Addresses retrieved successfully"
        )
    except Exception as e:
        return error_response(str(e), 500)


@addresses_bp.route('', methods=['POST'])
def create_address():
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return error_response("Missing user_id parameter", 400)
        
        data = request.get_json()
        
        required_fields = ['title', 'full_address', 'city', 'area', 'phone']
        if not data or not all(k in data for k in required_fields):
            return error_response("Missing required fields")
        
        # If setting as default, unset other default addresses
        if data.get('is_default', False):
            Address.query.filter_by(user_id=user_id, is_default=True).update({'is_default': False})
        
        address = Address(
            user_id=user_id,
            title=data['title'],
            full_address=data['full_address'],
            city=data['city'],
            area=data['area'],
            phone=data['phone'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            is_default=data.get('is_default', False)
        )
        
        db.session.add(address)
        db.session.commit()
        
        return success_response(address.to_dict(), "Address created successfully", 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


@addresses_bp.route('/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return error_response("Missing user_id parameter", 400)
        
        address = Address.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return error_response("Address not found", 404)
        
        data = request.get_json()
        
        # If setting as default, unset other default addresses
        if data.get('is_default', False):
            Address.query.filter_by(user_id=user_id, is_default=True).update({'is_default': False})
        
        if 'title' in data:
            address.title = data['title']
        if 'full_address' in data:
            address.full_address = data['full_address']
        if 'city' in data:
            address.city = data['city']
        if 'area' in data:
            address.area = data['area']
        if 'phone' in data:
            address.phone = data['phone']
        if 'latitude' in data:
            address.latitude = data['latitude']
        if 'longitude' in data:
            address.longitude = data['longitude']
        if 'is_default' in data:
            address.is_default = data['is_default']
        
        db.session.commit()
        
        return success_response(address.to_dict(), "Address updated successfully")
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


@addresses_bp.route('/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return error_response("Missing user_id parameter", 400)
        
        address = Address.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return error_response("Address not found", 404)
        
        db.session.delete(address)
        db.session.commit()
        
        return success_response(None, "Address deleted successfully")
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)
