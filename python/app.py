from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify, make_response
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from schemas import Credit, User, Payment
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import base64

app = Flask(__name__)

program = Flask(__name__)

engine = create_engine('mysql+mysqlconnector://root:Wight_wolf2000@127.0.0.1:3306/marta', echo=True)

ma = Marshmallow(app)


class CreditSchema(ma.Schema):
    class Meta:
        fields = ('credit_id', 'user_id', 'credit_limit', 'duration', 'credit_currency', 'passport_number')


class PaymentSchema(ma.Schema):
    class Meta:
        fields = ('payment_id', 'user_id', 'credit_id', 'payment', 'date')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'username', 'firstname', 'lastname', 'email', 'password', 'phone', 'user_status')


credit_Schema = CreditSchema()
credits_Schema = CreditSchema(many=True)

payment_Schema = PaymentSchema()
payments_Schema = PaymentSchema(many=True)

user_Schema = UserSchema()
users_Schema = UserSchema(many=True)

'''USER_REQUESTS'''


@app.route('/user', methods=['POST'])
def createUser():
    Session = sessionmaker(bind=engine)
    session = Session()

    request_data = request.json
    username = request_data["username"]
    firstname = request_data["firstname"]
    lastname = request_data["lastname"]
    email = request_data["email"]
    password = request_data["password"]
    phone = request_data["phone"]
    user_status = request_data["user_status"]

    new_user = User(username, firstname, lastname, email, password, phone, user_status)
    session.add(new_user)
    session.commit()
    return "added"


@app.route('/user/<id>', methods=['GET'])
def getUserById(id):
    Session = sessionmaker(bind=engine)
    session = Session()

    user = session.query(User).get(id)

    session.commit()
    return jsonify(user_Schema.dump(user))


@app.route('/user/<id>', methods=['PUT'])
def updateUserById(id):
    Session = sessionmaker(bind=engine)
    session = Session()

    request_data = request.json
    username = request_data["username"]
    firstname = request_data["firstname"]
    lastname = request_data["lastname"]
    email = request_data["email"]
    password = request_data["password"]
    phone = request_data["phone"]
    user_status = request_data["user_status"]

    session.query(User).filter_by(user_id=id).update(
        dict(username=username, firstname=firstname, lastname=lastname, email=email,
             password=password, phone=phone, user_status=user_status))

    user = session.query(User).get(id)
    session.commit()
    return jsonify(user_Schema.dump(user))


@app.route('/user/<id>', methods=['DELETE'])
def deleteUser(id):
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(User).filter_by(user_id=id).delete()
    session.commit()
    return "deleted"


'''CREDIT_REQUESTS'''


@app.route('/credit', methods=['POST'])
def createCredit():
    Session = sessionmaker(bind=engine)
    session = Session()

    request_data = request.json
    user_id = request_data["user_id"]
    credit_limit = request_data["credit_limit"]
    duration = request_data["duration"]
    credit_currency = request_data["credit_currency"]
    passport_number = request_data["passport_number"]

    new_credit = Credit(user_id, credit_limit, duration, credit_currency, passport_number)
    session.add(new_credit)
    session.commit()
    return "added"


@app.route('/credit/<id>', methods=['GET'])
def getCreditById(id):
    Session = sessionmaker(bind=engine)
    session = Session()

    credit = session.query(Credit).get(id)
    session.commit()
    return jsonify(credit_Schema.dump(credit))


@app.route('/credit/<id>', methods=['PUT'])
def updateCreditById(id):
    Session = sessionmaker(bind=engine)
    session = Session()

    request_data = request.json
    user_id = request_data["user_id"]
    credit_limit = request_data["credit_limit"]
    duration = request_data["duration"]
    credit_currency = request_data["credit_currency"]
    passport_number = request_data["passport_number"]

    session.query(Credit).filter_by(credit_id=id).update(
        dict(user_id=user_id, credit_limit=credit_limit, duration=duration, credit_currency=credit_currency,
             passport_number=passport_number))

    credit = session.query(Credit).get(id)
    session.commit()
    return jsonify(credit_Schema.dump(credit))


@app.route('/credit/<id>', methods=['DELETE'])
def deleteCredit(id):
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Credit).filter_by(credit_id=id).delete()
    session.commit()
    return "deleted"


'''PAYMENT_REQUEST'''

@app.route('/payment', methods=['POST'])
def createPayment():
    Session = sessionmaker(bind=engine)
    session = Session()

    request_data = request.json
    user_id = request_data["user_id"]
    credit_id = request_data["credit_id"]
    payment = request_data["payment"]
    date = request_data["date"]

    new_credit = Payment(user_id, credit_id, payment, date)
    session.add(new_credit)
    session.commit()
    return "added"


@app.route('/payment/<id>', methods=['GET'])
def getPaymentById(id):
    Session = sessionmaker(bind=engine)
    session = Session()

    payment = session.query(Payment).get(id)
    session.commit()
    return jsonify(payment_Schema.dump(payment))


@app.route('/payment/<id>', methods=['PUT'])
def updatePaymentById(id):
    Session = sessionmaker(bind=engine)
    session = Session()

    request_data = request.json
    user_id = request_data["user_id"]
    credit_id = request_data["credit_id"]
    payment = request_data["payment"]
    date = request_data["date"]

    session.query(Payment).filter_by(payment_id=id).update(
        dict(user_id=user_id, credit_id=credit_id, payment=payment, date=date))

    credit = session.query(Payment).get(id)
    session.commit()
    return jsonify(payment_Schema.dump(credit))


@app.route('/payment/<id>', methods=['DELETE'])
def deletePayment(id):
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Payment).filter_by(payment_id=id).delete()
    session.commit()
    return "deleted"


'''ERROR_HANDLING'''

@app.errorhandler(400)
def handle_400_error(e):
    return make_response(jsonify({'error': 'Bad  request'}), 400)


@app.errorhandler(404)
def handle_404_error(e):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def handle_405_error(e):
    return make_response(jsonify({'error': 'Method not allowed'}))


@app.errorhandler(500)
def handle_500_error(e):
    return make_response(jsonify({'error': 'Internal Server Error'}))


if __name__ == '__main__':
    app.run()

server = WSGIServer(('127.0.0.1', 5000), program)
server.serve_forever()
