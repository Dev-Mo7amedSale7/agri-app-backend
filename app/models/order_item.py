from datetime import datetime
from app.extensions import db


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)  # Snapshot of product name
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)  # Snapshot of price
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'quantity': self.quantity,
            'total_price': float(self.total_price) if self.total_price else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
