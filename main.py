from sqlalchemy import create_engine, Column, Integer, Date, VARCHAR, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import datetime



engine=create_engine('postgresql://postgres:5528@localhost:5432/l6', echo=False)
Session=sessionmaker(bind=engine)
session=Session()

Base=declarative_base()


'''Credit{
id	integer($int64)
userId	integer($int64)
creditLimit	string
duration	string($date-time)
creditCurrency	string
passport number	integer($int64)
 
}'''
class  Credit(Base):
    __tablename__='Credit'

    credit_id=Column(Integer,primary_key=True)
    user_id=Column(Integer, ForeignKey("User.user_id"))
    credit_limit=Column(Integer)
    duration=Column(Date)
    credit_currency=Column(VARCHAR(20))
    passport_number=Column(Integer)



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
class  User(Base):
    __tablename__='User'

    user_id=Column(Integer,primary_key=True)
    username=Column(VARCHAR(20))
    firstname=Column(VARCHAR(20))
    lastname=Column(VARCHAR(20))
    email=Column(VARCHAR(20))
    password=Column(VARCHAR(20))
    phone=Column(Integer)
    user_status=Column(VARCHAR(30))




''''Payment{
id	integer($int64)
userId	integer($int64)
creditId	string
payment	integer($int64)
date	string($date-time)
 
}
'''
class  Payment(Base):
    __tablename__='Payment'


    payment_id=Column(Integer,primary_key=True)
    user_id=Column(Integer, ForeignKey("User.user_id"))
    credit_id=Column(Integer, ForeignKey("Credit.credit_id"))
    payment=Column(Integer)
    date=Column(Date)



#Base.metadata.create_all(engine)


'''user1=User(user_id=1, username='u1',firstname='Oleg', lastname='Kalush',email='kalusholeg@gmail.com', password='pw1', phone=569,user_status='wmp')
user2=User(user_id=2, username='u2',firstname='Anna', lastname='Ogienko',email='ogienkivna@gmail.com', password='pw2', phone=921,user_status='mpd')
user3=User(user_id=3, username='u3',firstname='Victor', lastname='Baraniak',email='victorbar@gmail.com', password='pw3', phone=111,user_status='u')

session.add(user1)
session.add(user2)
session.add(user3)
'''

'''
cr1=Credit(credit_id=1, user_id=1,credit_limit=50000, duration='11-02-2018', credit_currency='$',  passport_number=1578)
cr2=Credit(credit_id=2, user_id=2,credit_limit=100000, duration='01-12-2021', credit_currency='грн',   passport_number=1693)
cr3=Credit(credit_id=3, user_id=3,credit_limit=1000, duration='05-11-2019', credit_currency='грн',   passport_number=2056947)
cr4=Credit(credit_id=4, user_id=2,credit_limit=25900, duration='06-12-2005', credit_currency='$',   passport_number=36951)

session.add(cr1)
session.add(cr2)
session.add(cr3)
session.add(cr4)

session.commit()
'''
#s=session.query(Payment)

'''''
p1=Payment(payment_id=1,user_id=1,credit_id=1, payment=256,date='15-01-2016')
p2=Payment(payment_id=2,user_id=1,credit_id=1, payment=256,date='15-02-2016')
p3=Payment(payment_id=3,user_id=2,credit_id=2, payment=1000,date='01-02-2020')
p4=Payment(payment_id=4,user_id=2,credit_id=2, payment=100,date='01-03-2020')
p5=Payment(payment_id=5,user_id=2,credit_id=3, payment=95,date='01-05-2018')
p6=Payment(payment_id=6,user_id=2,credit_id=3, payment=95,date='01-06-2018')
p7=Payment(payment_id=7,user_id=3,credit_id=4, payment=2500,date='01-05-2003')

session.add_all([p1,p2,p3,p4,p5,p6,p7])
session.commit()
'''
#for s1 in s:
#    print(s1.payment_id, s1.payment, s1.date)



