from flask import Blueprint
from app.extensions import db
from app.models.category import Category
from app.models.product import Product
from app.utils.responses import success_response, error_response

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        return success_response(
            [category.to_dict() for category in categories],
            "Categories retrieved successfully"
        )
    except Exception as e:
        return error_response(str(e), 500)


@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return error_response("Category not found", 404)
        
        return success_response(category.to_dict(), "Category retrieved successfully")
    except Exception as e:
        return error_response(str(e), 500)


@categories_bp.route('/<int:category_id>/products', methods=['GET'])
def get_category_products(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return error_response("Category not found", 404)
        
        products = Product.query.filter_by(
            category_id=category_id,
            is_available=True
        ).all()
        
        return success_response(
            [product.to_dict() for product in products],
            "Category products retrieved successfully"
        )
    except Exception as e:
        return error_response(str(e), 500)
