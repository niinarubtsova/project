import json

from flask import Flask, request
from flask_sqlalchemy import  SQLAlchemy

import raw_data

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(255))
    role = db.Column(db.String(255))
    phone = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String())
    end_date = db.Column(db.String())
    address = db.Column(db.String(255))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


#--------------------------------Users Views--------------------------------------

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "GET":
        result = []
        for u in User.query.all():
            result.append(u.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )

        db.session.add(new_user)
        db.session.commit()

        return "User created", 201

@app.route("/user/<int:uid>", methods=["GET", "PUT", "DELETE"])
def users(uid: int):

    if request.method == "GET":
        return json.dumps(User.query.get(uid).to_dict()), 200

    if request.method == "PUT":
        user_data = json.loads(request.data)
        u = User.query.get(uid)
        u.first_name = user_data["first_name"]
        u.last_name = user_data["last_name"]
        u.age = user_data["age"]
        u.email = user_data["email"]
        u.role = user_data["role"]
        u.phone = user_data["phone"]

        db.session.add(u)
        db.session.commit()

        return "User updated", 204

    if request.method == "DELETE":
        u = User.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "User delete", 204


#---------------------------------Orders Views--------------------------------

@app.route("/order", methods=["GET", "POST"])
def order():
    if request.method == "GET":
        result = []
        for u in Order.query.all():
            result.append(u.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        order_data = json.loads(request.data)
        new_order = Order(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"],
        )

        db.session.add(new_order)
        db.session.commit()

        return "Order Created", 201

@app.route("/order/<int:uid>", methods=["GET", "PUT", "DELETE"])
def orders(uid: int):
    if request.method == "GET":
        return json.dumps(Order.query.get(uid).to_dict()), 200

    if request.method == "PUT":
        order_data = json.loads(request.data)
        u = Order.query.get(uid)
        u.name = order_data["name"]
        u.description = order_data["description"]
        u.start_date = order_data["start_date"]
        u.end_date = order_data["end_date"]
        u.address = order_data["address"]
        u.price = order_data["price"]
        u.customer_id = order_data["customer_id"]
        u.executor_id = order_data["executor_id"]

        db.session.add(u)
        db.session.commit()

        return "Order updated", 204

    if request.method == "DELETE":
        u = Order.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "Order delete", 204


#---------------------------------Offers Views------------------------------

@app.route("/offer", methods=["GET", "POST"])
def offer():
    if request.method == "GET":
        result = []
        for u in Offer.query.all():
            result.append(u.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        offer_data = json.loads(request.data)
        new_offer = Offer(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"],
        )

        db.session.add(new_offer)
        db.session.commit()

        return "Offer Created", 201

@app.route("/offer/<int:uid>", methods=["GET", "PUT", "DELETE"])
def offers(uid: int):
    if request.method == "GET":
        return json.dumps(Offer.query.get(uid).to_dict()), 200

    if request.method == "PUT":
        offer_data = json.loads(request.data)
        u = Offer.query.get(uid)
        u.order_id = offer_data["order_id"]
        u.executor_id = offer_data["executor_id"]

        db.session.add(u)
        db.session.commit()

        return "Offer updated", 204

    if request.method == "DELETE":
        u = Offer.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "Offer delete", 204


#---------------------------------Init DB----------------------------------

def init_database():
    db.drop_all()
    db.create_all()

    for user_data in raw_data.users:
        new_user = User(
            id = user_data["id"],
            first_name =  user_data["first_name"],
            last_name = user_data["last_name"],
            age = user_data["age"],
            email = user_data["email"],
            role = user_data["role"],
            phone = user_data["phone"],
        )

        db.session.add(new_user)
        db.session.commit()

    for order_data in raw_data.orders:
        new_order = Order(
            id = order_data["id"],
            name = order_data["name"],
            description = order_data["description"],
            start_date = order_data["start_date"],
            end_date = order_data["end_date"],
            address = order_data["address"],
            price = order_data["price"],
            customer_id = order_data["customer_id"],
            executor_id = order_data["executor_id"],
        )

        db.session.add(new_order)
        db.session.commit()


    for offer_data in raw_data.offers:
        new_offer = Offer(
            id = offer_data["id"],
            order_id = offer_data["order_id"],
            executor_id = offer_data["executor_id"],
        )

        db.session.add(new_offer)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        init_database()
        app.run(debug=True)
