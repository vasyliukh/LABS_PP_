import datetime
import os
import sys
import json
from functools import wraps
from http import client
import requests
from sqlalchemy import *
from base.base import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
sys.path.append('..')
import bcrypt
import jwt
import pytest
from flask import Flask, jsonify, request, make_response, session
from flask_bcrypt import check_password_hash
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from requests import api
from sqlalchemy.future import engine
from sqlalchemy import   engine
from sqlalchemy import create_engine
from sqlalchemy import create_engine, Column, Integer, Sequence, String, Date, Float, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

session=sessionmaker(bind=engine)

s = session()


app = Flask(__name__)
app.config['SECRET_KEY'] ='my secret key'


@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})


besedir = os.path.abspath(os.path.dirname(__file__))
sqldb = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5528@localhost:5432/ul'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
engine = create_engine('postgresql://postgres:5528@localhost:5432/ul', echo=True)

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


    new_payment = Payment(user_id, credit_id, payment, date)
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


'''''
def func(x):
    return x+5


def test_method3():
    liist=[1,2,3]
    assert  1 in liist


def test_method1():
    liist=[1,2,3]
    assert  3 in liist

def test_method2():
    liist=[1,2,3]
    assert  5 in liist






@pytest.fixture(scope='function')
def session(app):
    ctx=app.app_context()
    ctx.push()

    yield session
    session.close_all()
    ctx.pop()


@pytest.fixture(scope='function')
def user(session):
    user=User(
        username='user1',
        userStatus='dk',
        firstName='Alex',
        lastName='Bing',
        phone='0501236954',
        password='5528',
        email='userok@gmail.com'
    )
    session.add(user)
    session.commit()

    return user



def test_model(user):
    assert user.username=='huink'

'''

user1=User(username="user1", firstName="Olersandr", lastName="filiponov", userStatus="user", email="user@gmail.com", phone="05641489", password="1649")
user2=User(username="user2", firstName="Anna", lastName="Horibna", userStatus="user", email="horib@gmail.com", phone="05056941325", password="5528")


def test_register_user():
    client = app.test_client()
    url = "http://127.0.0.1:5000/User"

    # user_data_json = "{\n    \"firstName\": \"FirstName\",\n    \"lastName\": \"LastName\",\n    \"username\": " \
    #                  "\"username\",\n    \"password\": \"pass\" \n} "
    user_data = {"username": "user8", "password": "user3", "lastName": "name8", "firstName": "name3", "phone": "05164961468",
         "status": "user", "email":"ebfhew@gmail.com"}
    user_data2 = {"username": "user154", "password": "pw1", "lastName": "nih", "firstName": "whyegf", "phone": "06632147896",
         "status": "user", "email":"nhygtgh@gmail.com"}

    headers = {
        'Content-Type': 'application/json'
    }
    resp = requests.post(url, headers=headers, data=json.dumps(user_data2))
    assert resp.status_code == 400

    resp = requests.post(url, headers=headers, data=json.dumps(user_data))
    user = s.query(User).filter_by(username="user8").first()
    assert resp.status_code == 200
    assert user.ClientName == "name8"
    s.delete(user)
    s.commit()

@pytest.fixture(scope="module")
def create_user():
    user = User(username="user1", firstName="Olersandr", lastName="filiponov", userStatus="user", email="user@gmail.com", phone="05641489", password="1649")
    s.add(user)
    s.commit()
    yield
    s.delete(user)
    s.commit()



def test_login_user(create_user):
    client = app.test_client()
    url = "http://127.0.0.1:5000/login"

    login_data_json = "{\n    \"username\": \"user1\",\n   \"password\": \"user1\" \n} "

    non_password = "{\n    \"username\": \"user1\" \n} "

    user_data = {"username": "nouser", "password": "user1"}

    non_existing_user_json = "{\n    \"username\": \"user01\",\n   \"password\": \"user1\" \n} "

    not_matching_password_json = "{\n    \"username\": \"user1\",\n   \"password\": \"invalid\" \n} "

    headers = {
        'Content-Type': 'application/json'
    }

    resp = client.post(url, headers=headers, data=login_data_json)
    assert resp.status_code == 200

    resp = client.post(url, headers=headers, data=non_password)

    assert resp.status_code == 401

    resp = client.post(url, headers=headers, data=not_matching_password_json)

    assert resp.status_code == 401

    resp = client.post(url, headers=headers, data=json.dumps(user_data))
    assert resp.status_code == 404


@pytest.fixture()
def login_user(create_user):
    login_data_json = "{\n    \"username\": \"user1\",\n   \"password\": \"user1\" \n} "
    test_client = app.test_client()
    url = 'http://127.0.0.1:5000/auth/login'
    headers = {
        'Content-Type': 'application/json'
    }
    resp = test_client.post(url, headers=headers, data=login_data_json)
    access_token_data_json = json.loads(resp.get_data(as_text=True))
    return access_token_data_json


Database={
    1:["Olex", 11],
    2:["Oleg", 20],
    3:["Alina", 0.3],
    4:["Olga", 8]
}

def read_player(play):
    id=play['Player_id']
    if id in Database:
        entry=Database[id]
        return{
            "Code":200,
            "Responce":{"Name": entry[0],"Age":entry[1] },
            "Messsage":"Succesful read"
        }
    else:
        return {"Code":404, "Message":"The object doesnt exist"}

test_playload={
    "Player_id":4
}
def test_read_player():
    response=read_player(test_playload)
    assert response.get("Code")==200

@pytest.fixture(scope='function')
def adduser():
    session = sessionmaker(bind=engine)
    session = Session()
    user=User(username="user1",
              firstName="Olersandr",
              lastName="filiponov",
              userStatus="user",
              email="user@gmail.com",
              phone="05641489",
              password="1649"
    )
    db.session.add(user)
    db.session.commit()

    return user


def testt(adduser):
    assert adduser.username=='user1'



@pytest.fixture()
def login_user(adduser):
    login_data_json = "{\n    \"username\": \"user1\",\n   \"password\": \"user1\" \n} "
    test_client = app.test_client()
    url = 'http://127.0.0.1:5000/login'
    headers = {
        'Content-Type': 'application/json'
    }
    resp = test_client.post(url, headers=headers, data=login_data_json)
    access_token_data_json = json.loads(resp.get_data(as_text=True))
    return access_token_data_json


def test_registerrr_user():
    client = app.test_client()
    request_params = {
        "username": "username",
        "firstName": "Oleksiy",
        "lastName": "Vasiuta",
        "userStatus": "u",
        'email': 'user@gmail.com',
        'phone': '05641489',
        'password': '1649'
    }

    response = client.post(
        '/register',
        json=request_params
    )
    assert response.status_code == 201


if __name__ == '__main__':
    app.run(debug=True)
    print("---------------")


def create_app():
    test = app.test_client()
    return test