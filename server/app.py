# server/app.py

from flask import Flask, request, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

# create a Flask application instance 
app = Flask(__name__)

# configure the database connection to the local file app.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# configure flag to disable modification tracking and use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)


# ---------------------------
# ROUTES
# ---------------------------

# POST /baked_goods → create a new baked good
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    title = request.form.get("title")
    price = request.form.get("price")
    bakery_id = request.form.get("bakery_id")

    if not title or not price or not bakery_id:
        return jsonify({"error": "Missing required fields"}), 400

    new_good = BakedGood(title=title, price=price, bakery_id=bakery_id)
    db.session.add(new_good)
    db.session.commit()

    return jsonify(new_good.to_dict()), 201


# PATCH /bakeries/<int:id> → update bakery name
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)

    if not bakery:
        return jsonify({"error": "Bakery not found"}), 404

    name = request.form.get("name")
    if name:
        bakery.name = name

    db.session.commit()
    return jsonify(bakery.to_dict()), 200


# DELETE /baked_goods/<int:id> → delete baked good
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if not baked_good:
        return jsonify({"error": "Baked good not found"}), 404

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({"message": "Baked good deleted successfully"}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)

