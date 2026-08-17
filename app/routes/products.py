from flask import Blueprint, request
from app.services.product_service import ProductService
from app.utils.responses import success_response, error_response

products_bp = Blueprint('products', __name__)


@products_bp.route('', methods=['GET'])
def get_products():
    try:
        search = request.args.get('search')
        category_id = request.args.get('category_id', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = ProductService.get_products(search, category_id, page, per_page)
        
        return success_response({
            'products': [product.to_dict() for product in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        }, "Products retrieved successfully")
        
    except Exception as e:
        return error_response(str(e), 500)


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = ProductService.get_product(product_id)
        if not product:
            return error_response("Product not found", 404)
        
        return success_response(product.to_dict(), "Product retrieved successfully")
        
    except Exception as e:
        return error_response(str(e), 500)
