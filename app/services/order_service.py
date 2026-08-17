from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.address import Address
from flask import current_app
from decimal import Decimal


class OrderService:
    @staticmethod
    def create_order(user, address_id, payment_method, notes, items):
        try:
            # Validate address
            address = Address.query.filter_by(id=address_id, user_id=user.id).first()
            if not address:
                return None, "Address not found"
            
            # Validate items and calculate totals
            subtotal = Decimal('0')
            for item in items:
                product = Product.query.get(item['product_id'])
                if not product:
                    return None, f"Product {item['product_id']} not found"
                if not product.is_available:
                    return None, f"Product {product.name} is not available"
                if item['quantity'] > product.available_quantity:
                    return None, f"Insufficient stock for {product.name}"
                if item['quantity'] <= 0:
                    return None, f"Invalid quantity for {product.name}"
                
                # Use current price from database
                unit_price = product.price
                item_total = unit_price * item['quantity']
                subtotal += item_total
            
            # Calculate delivery fee and total
            delivery_fee = Decimal(str(current_app.config['DELIVERY_FEE']))
            total = subtotal + delivery_fee
            
            # Create order within transaction
            try:
                order = Order(
                    user_id=user.id,
                    address_id=address_id,
                    subtotal=subtotal,
                    delivery_fee=delivery_fee,
                    total=total,
                    payment_method=payment_method,
                    status='pending',
                    notes=notes
                )
                db.session.add(order)
                db.session.flush()  # Get order ID
                
                # Create order items and decrease stock
                for item in items:
                    product = Product.query.get(item['product_id'])
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=item['product_id'],
                        product_name=product.name,
                        unit_price=product.price,
                        quantity=item['quantity'],
                        total_price=product.price * item['quantity']
                    )
                    db.session.add(order_item)
                    
                    # Decrease stock
                    product.available_quantity -= item['quantity']
                
                db.session.commit()
                return order, None
            except Exception as e:
                db.session.rollback()
                return None, str(e)
                
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def cancel_order(order):
        try:
            # Check if order can be cancelled
            if order.status not in ['pending', 'confirmed']:
                return False, "Order cannot be cancelled in current status"
            
            # Restore stock
            for item in order.items:
                product = Product.query.get(item.product_id)
                if product:
                    product.available_quantity += item.quantity
            
            # Update order status
            order.status = 'cancelled'
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def update_order_status(order, new_status):
        try:
            order.status = new_status
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
