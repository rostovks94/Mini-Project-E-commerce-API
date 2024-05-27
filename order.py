from models import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)

    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f'<Order {self.id}>'