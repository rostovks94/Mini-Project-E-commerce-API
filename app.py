from flask_sqlalchemy import SQLAlchemy
from models.customer import Customer
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/ecommerce_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')

    if not name or not email or not phone_number:
        return jsonify({'error': 'Missing required fields'}), 400

    new_customer = Customer(name=name, email=email, phone_number=phone_number)
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({'message': 'Customer created successfully'}), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customers_data = [{'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone_number': customer.phone_number} for customer in customers]
    return jsonify(customers_data)

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    customer_data = {'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone_number': customer.phone_number}
    return jsonify(customer_data)

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone_number = data.get('phone_number', customer.phone_number)

    db.session.commit()

    return jsonify({'message': 'Customer updated successfully'})

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({'message': 'Customer deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)