import base64

import bcrypt
from sqlalchemy import Column, Integer, Date, VARCHAR, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import sha256_crypt

Base = declarative_base()

'''Credit{
id	integer($int64)
userId	integer($int64)
creditLimit	string
duration	string($date-time)
creditCurrency	string
passport number	integer($int64)
 
}'''


class Credit(Base):
    __tablename__ = 'Credit'

    credit_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    credit_limit = Column(Integer)
    duration = Column(Date)
    credit_currency = Column(VARCHAR(20))
    passport_number = Column(Integer)

    def __init__(self, user_id, credit_limit, duration, credit_currency, passport_number):
        self.credit_id = None
        self.user_id = user_id
        self.credit_limit = credit_limit
        self.duration = duration
        self.credit_currency = credit_currency
        self.passport_number = passport_number



'''User{
id	integer($int64)
username	string
firstName	string
lastName	string
email	string
password	string
phone	string
userStatus	integer($int32)
User Status

 
}'''


class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(20))
    firstname = Column(VARCHAR(20))
    lastname = Column(VARCHAR(20))
    email = Column(VARCHAR(20))
    password = Column(VARCHAR(100))
    phone = Column(Integer)
    user_status = Column(VARCHAR(30))

    def __init__(self, username, firstname, lastname, email, password, phone, user_status):
        self.user_id = None
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

        self.password = bcrypt.hashpw(password.encode('utf-8','ignore'), bcrypt.gensalt())
        self.phone = phone
        self.user_status = user_status

''''Payment{
id	integer($int64)
userId	integer($int64)
creditId	string
payment	integer($int64)
date	string($date-time)
 
}
'''


class Payment(Base):
    __tablename__ = 'Payment'

    payment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    credit_id = Column(Integer, ForeignKey("Credit.credit_id"))
    payment = Column(Integer)
    date = Column(Date)

    def __init__(self, user_id, credit_id, payment, date):
        self.payment_id = None
        self.user_id = user_id
        self.credit_id = credit_id
        self.payment = payment
        self.date = date

# Base.metadata.create_all(engine)
