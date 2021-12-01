import datetime

import bcrypt
import jwt
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy import String, Integer, ForeignKey, Date, BOOLEAN
from flask_bcrypt import check_password_hash
from functools import wraps
app = Flask(__name__)
app.config['SECRET_KEY'] ='my secret key'


@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})


besedir = os.path.abspath(os.path.dirname(__file__))
sqldb = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:fd546ut81w@localhost:3306/l6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    tablename = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    userStatus = db.Column(db.String(20), nullable=False)

    def __init__(self, username, firstName, lastName, email, password, phone, userStatus):
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.phone = phone
        self.userStatus = userStatus
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'firstName', 'lastName', 'email', 'password', 'phone', 'userStatus')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
@app.route('/User', methods=['POST'])

def add_user():
    username = request.json['username']
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']
    phone = request.json['phone']
    userStatus = request.json['userStatus']

    hased = bcrypt.hashpw(password.encode('utf-8', 'ignore'), bcrypt.gensalt())

    new_user = User(username, firstName, lastName, email, hased, phone, userStatus)

    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@app.route('/User', methods=['GET'])
@token_required
def get_users(current_user):
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/User/<id>', methods=['GET'])
@token_required
def get_user(current_user,id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


@app.route('/User/<id>', methods=['PUT'])
@token_required
def update_user(current_user,id):
    user = User.query.get(id)


    username = request.json['username']
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']
    phone = request.json['phone']
    userStatus = request.json['userStatus']


    user.username = username
    user.firstName = firstName
    user.lastName = lastName
    user.email = email
    user.password = password
    user.phone = phone
    user.userStatus = userStatus
    db.session.commit()
    return user_schema.jsonify(user)


@app.route('/User/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/login',methods=['GET'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
#___________________Credit__________________#

class Credit(db.Model):
    __tablename__='Credit'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    duration = db.Column(db.Float, nullable=False)
    credit_limit = db.Column(db.Integer,nullable=False)
    credit_currency = db.Column(db.String(20),nullable=False)
    passport_number = db.Column(db.Integer,nullable=False)

    def __init__(self, user_id, credit_limit, duration, credit_currency, passport_number):
        self.user_id = user_id
        self.credit_limit = credit_limit
        self.duration= duration
        self.credit_currency = credit_currency
        self.passport_number = passport_number



class CreditSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'credit_limit','duration', 'credit_currency', 'passport_number')


credit_schema = CreditSchema()
credits_schema = CreditSchema(many=True)

@app.route('/Credit', methods=['POST'])
def add_credit():

    user_id = request.json["user_id"]
    credit_limit = request.json["credit_limit"]
    duration = request.json["duration"]
    credit_currency = request.json["credit_currency"]
    passport_number = request.json["passport_number"]

    new_credit = Credit(user_id, credit_limit, duration, credit_currency, passport_number)
    db.session.add(new_credit)
    db.session.commit()
    return credit_schema.jsonify(new_credit)

@app.route('/Credit', methods=['GET'])
def get_credits():
    all_credits = Credit.query.all()
    result = users_schema.dump(all_credits )
    return jsonify(result)

@app.route('/Credit/<id>', methods=['GET'])
def get_credit(id):
    credit = Credit.query.get(id)
    return credit_schema.jsonify(credit)

@app.route('/Credit/<id>', methods=['PUT'])
def update_credit(id):
    credit = Credit.query.get(id)
    user_id = request.json["user_id"]
    credit_limit = request.json["credit_limit"]
    duration = request.json["duration"]
    credit_currency = request.json["credit_currency"]
    passport_number = request.json["passport_number"]

    credit.user_id = user_id
    credit.credit_limit = credit_limit
    credit.duration = duration
    credit.credit_currency = credit_currency
    credit.passport_number = passport_number
    db.session.commit()
    return credit_schema.jsonify(credit)

@app.route('/Credit/<id>', methods=['DELETE'])
def delete_credit(id):
    credit = Credit.query.get(id)
    db.session.delete(credit)
    db.session.commit()
    return user_schema.jsonify(credit)
#__________Payment_______________#
class Payment(db.Model):
    __tablename__ = 'Payment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    credit_id = db.Column(db.Integer, db.ForeignKey("Credit.id"))
    payment =db.Column(db.Integer,nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, user_id, credit_id, payment, date):
        self.user_id = user_id
        self.credit_id = credit_id
        self.payment = payment
        self.date = date
class PaymentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'credit_id','payment', 'date')


payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)
@app.route('/Payment', methods=['POST'])
def add_payment():

    user_id = request.json["user_id"]
    credit_id = request.json["credit_id"]
    payment = request.json["payment"]
    date = request.json["date"]

    new_payment = Credit(user_id, credit_id, payment, date)
    db.session.add(new_payment)
    db.session.commit()
    return credit_schema.jsonify(new_payment)

@app.route('/Payment', methods=['GET'])
def get_payments():
    all_payments = Payment.query.all()
    result = payments_schema.dump(all_payments )
    return jsonify(result)
@app.route('/Payment/<id>', methods=['GET'])
def get_payment(id):
    payment = Payment.query.get(id)
    return payment_schema.jsonify(payment)

@app.route('/Payment/<id>', methods=['PUT'])
def update_payment(id):
    payment = Payment.query.get(id)
    user_id = request.json["user_id"]
    credit_id = request.json["credit_id"]
    payment = request.json["payment"]
    date = request.json["date"]

    payment.user_id = user_id
    payment.credit_id = credit_id
    payment.payment = payment
    payment.date = date

    db.session.commit()
    return credit_schema.jsonify(payment)
@app.route('/Payment/<id>', methods=['DELETE'])
def delete_payment(id):
    payment = Payment.query.get(id)
    db.session.delete(payment)
    db.session.commit()
    return user_schema.jsonify(payment)

if __name__ == '__main__':
    app.run()