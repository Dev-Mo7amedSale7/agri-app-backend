from app.extensions import db
from app.models.product import Product
from app.models.category import Category


class ProductService:
    @staticmethod
    def get_products(search=None, category_id=None, page=1, per_page=20):
        query = Product.query
        
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        query = query.filter_by(is_available=True)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination
    
    @staticmethod
    def get_product(product_id):
        return Product.query.get(product_id)
    
    @staticmethod
    def create_product(data):
        try:
            # Validate category exists
            category = Category.query.get(data['category_id'])
            if not category:
                return None, "Category not found"
            
            product = Product(
                name=data['name'],
                description=data.get('description'),
                price=data['price'],
                unit=data['unit'],
                image_url=data.get('image_url'),
                category_id=data['category_id'],
                available_quantity=data.get('available_quantity', 0),
                is_available=data.get('is_available', True)
            )
            db.session.add(product)
            db.session.commit()
            return product, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_product(product_id, data):
        try:
            product = Product.query.get(product_id)
            if not product:
                return None, "Product not found"
            
            # Validate category if provided
            if 'category_id' in data:
                category = Category.query.get(data['category_id'])
                if not category:
                    return None, "Category not found"
                product.category_id = data['category_id']
            
            if 'name' in data:
                product.name = data['name']
            if 'description' in data:
                product.description = data['description']
            if 'price' in data:
                product.price = data['price']
            if 'unit' in data:
                product.unit = data['unit']
            if 'image_url' in data:
                product.image_url = data['image_url']
            if 'available_quantity' in data:
                product.available_quantity = data['available_quantity']
            if 'is_available' in data:
                product.is_available = data['is_available']
            
            db.session.commit()
            return product, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_product(product_id):
        try:
            product = Product.query.get(product_id)
            if not product:
                return None, "Product not found"
            
            db.session.delete(product)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_stock(product_id, quantity):
        try:
            product = Product.query.get(product_id)
            if not product:
                return None, "Product not found"
            
            if quantity < 0:
                return None, "Quantity cannot be negative"
            
            product.available_quantity = quantity
            db.session.commit()
            return product, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_availability(product_id, is_available):
        try:
            product = Product.query.get(product_id)
            if not product:
                return None, "Product not found"
            
            product.is_available = is_available
            db.session.commit()
            return product, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
