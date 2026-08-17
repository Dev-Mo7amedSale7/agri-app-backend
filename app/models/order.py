from datetime import datetime
from app.extensions import db


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    delivery_fee = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False, default='cash_on_delivery')
    status = db.Column(db.String(50), nullable=False, default='pending', index=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'address_id': self.address_id,
            'subtotal': float(self.subtotal) if self.subtotal else 0,
            'delivery_fee': float(self.delivery_fee) if self.delivery_fee else 0,
            'total': float(self.total) if self.total else 0,
            'payment_method': self.payment_method,
            'status': self.status,
            'notes': self.notes,
            'items': [item.to_dict() for item in self.items],
            'address': self.address.to_dict() if self.address else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
