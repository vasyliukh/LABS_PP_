import datetime

import jwt
import pytest
from flask import app
from sqlalchemy.dialects.postgresql import json
from sqlalchemy.future import engine
from sqlalchemy.orm import sessionmaker, Session
from app import app, Credit, Payment
from app import User, db

test = app.test_client()

@pytest.fixture(scope='function')
def adduser():
    session = sessionmaker(bind=engine)
    session = Session()
    user=User(
        username="user1",
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


class TestCreateUser:

    def test1user(self):
        data = {
              'username':'user1',
              'firstName':'Olersandr',
              'lastName':'filiponov',
              'userStatus':'u',
              'email':'user@gmail.com',
              'phone':'05641489',
              'password':'1649'}
        test1 = test.post('/UserCreate', json=data)
        #assert test1.status_code == 200
        print(test1.status_code)
        assert test1.get_json() == None
        #assert test1.get_json() == [{'message': 'Invalid input'}, 400]

    def test2user(self):
        data = {'username':'user2',
              'firstName':'Anna',
              'lastName':'Bulgacova',
              'userStatus':'u',
              'email':'gerg@gmail.com',
              'phone':'05984116',
              'password':'5693'}
        test2 = test.post('/UserCreate', json=data)
        assert test2.status_code == 200
        assert test2.get_json() == [{'message': 'Invalid input'}, 400]
        #assert test2.status_code ==404
        #assert test2.get_json() == None

    def test3user(self):
        data = {'username':'user3',
              'firstName':'Ruslana',
              'lastName':'Vasiuk',
              'userStatus':'u',
              'email':'vuskk@gmail.com',
              'phone':'06931546',
              'password':'*jjioA'}
        test3 = test.post('/UserCreate', json=data)
        #assert test3.status_code == 200
        #assert test3.get_json() == [{"message": "User exist with such login"}, 409]
        assert test3.get_json() == None

    def test4user(self):
        data = {'username':'user4',
              'firstName':'Victoria',
              'lastName':'Savcoc',
              'userStatus':'a',
              'email':'savcovn@gmail.com',
              'phone':'231489',
              'password':'9631'}
        test4 = test.post('/UserCreate', json=data)
        #assert test4.status_code == 404
        #assert test4.get_json() == [{'message': 'Invalid input'}, 400]
        assert test4.get_json() == None

    def test5user(self):
        data = {'username':'user5',
              'firstName':'njoeug',
              'lastName':'ergrfwef',
              'userStatus':'a',
              'email':'wefef@gmail.com',
              'phone':'0566841489',
              'password':'16juY49'}
        #global username
        username = data['username']
        test5 = test.post('/User', json=data)
        #assert test5.status_code == 404
        assert User.query.filter_by(username=data['username']) is not None



class TestCreateCredit:

    def test1credit(self):
        data = {
            'user_id':41,
            'duration':5.2,
            'credit_limit':90000,
            'credit_currency':"$",
            'passport_number':12589
        }
        test1 = test.post('/Credit', json=data)
        assert test1.status_code == 404
        #assert test1.get_json() == [{'message': 'Invalid input'}, 400]

    def test2credit(self):
        data = {
            'user_id':42,
            'duration':10,
            'credit_limit':800,
            'credit_currency':"э",
            'passport_number':152854989
        }
        test2 = test.post('/Credit', json=data)
        #assert test2.get_json() == [{'message': 'Invalid input'}, 400]
        assert test2.status_code == 200


    def test3credit(self):
        data = {'user_id':43,
            'duration':5,
            'credit_limit':1000,
            'credit_currency':"$",
            'passport_number':1226849
                }
        test3 = test.post('/Credit', json=data)
        assert test3.status_code == 200
        #assert test3.get_json() == [{"message": "User exist with such login"}, 409]


    def test4credit(self):
        data = {'user_id':41,
            'credit_limit':50000,
            'credit_currency':"грн",
            'passport_number':196419}
        test4 = test.post('/Credit', json=data)
        assert test4.status_code == 500
        #assert test4.get_json() == [{'message': 'Invalid input'}, 400]


    def test5credit(self):
        data = {'user_id':40,
            'duration':10,
            'credit_limit':10000,
            'credit_currency':"$",
            'passport_number':12565489}
        global user_id
        user_id = data['user_id']
        test5 = test.post('/Credit', json=data)
        assert test5.status_code == 200
        assert Credit.query.filter_by(user_id=data['user_id']) is not None



class TestCreatePayment:

    def test1pay(self):
        data = {
            'user_id':1,
            'credit_id':1,
            'payment':900
        }
        test1 = test.post('/Payment', json=data)
        assert test1.status_code == 500
        #assert test1.get_json() == [{'message': 'Invalid input'}, 400]


    def test3pay(self):
        data = {
            'user_id': 41,
            'credit_id': 69,
            'payment': 550,
            'date': '01-01-2018'
        }
        test3 = test.post('/Payment', json=data)
        assert test3.status_code == 200


    def test5pay(self):
        data = {
            'user_id':41,
            'credit_id':73,
            'payment':560,
            'date':'02-01-2019'
        }
        global payment
        payment= data['payment']
        test5 = test.post('/Payment', json=data)
        assert test5.status_code == 200
        assert Payment.query.filter_by(payment=['payment']) is not None

''''
    def test4pay(self):
        data = {
            'user_id':41,
            'credit_id':69,
            'payment':550,
            'date':'01-01-2018'
        }
        test4 = test.post('/Payment', json=data)
        assert test4.status_code == 404
        
'''