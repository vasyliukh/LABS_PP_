from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from schemas import Credit, User, Payment

engine = create_engine('', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

user1 = User(username='u1', firstname='Oleg', lastname='Kalush', email='kalusholeg@gmail.com',
             password='pw1', phone=569, user_status='wmp')
user2 = User(username='u2', firstname='Anna', lastname='Ogienko', email='ogienkivna@gmail.com',
             password='pw2', phone=921, user_status='mpd')
user3 = User(username='u3', firstname='Victor', lastname='Baraniak', email='victorbar@gmail.com',
             password='pw3', phone=111, user_status='u')

session.add(user1)
session.add(user2)
session.add(user3)
session.commit()

cr1 = Credit(user_id=1, credit_limit=50000, duration='2018-02-11', credit_currency='$',
             passport_number=1578)
cr2 = Credit(user_id=2, credit_limit=100000, duration='2021-12-01', credit_currency='UAH',
             passport_number=1693)
cr3 = Credit(user_id=3, credit_limit=1000, duration='2019-11-05', credit_currency='UAH',
             passport_number=2056947)
cr4 = Credit(user_id=2, credit_limit=25900, duration='2005-12-06', credit_currency='$',
             passport_number=36951)

session.add(cr1)
session.add(cr2)
session.add(cr3)
session.add(cr4)

session.commit()

# s=session.query(Payment)


p1 = Payment(user_id=1, credit_id=1, payment=256, date='2016-01-05')
p2 = Payment(user_id=1, credit_id=1, payment=256, date='2016-02-15')
p3 = Payment(user_id=2, credit_id=2, payment=1000, date='2020-02-01')
p4 = Payment(user_id=2, credit_id=2, payment=100, date='2020-03-01')
p5 = Payment(user_id=2, credit_id=3, payment=95, date='2018-05-01')
p6 = Payment(user_id=2, credit_id=3, payment=95, date='2018-06-01')
p7 = Payment(user_id=3, credit_id=4, payment=2500, date='2003-05-01')

session.add_all([p1, p2, p3, p4, p5, p6, p7])
session.commit()

# for s1 in s:
#    print(s1.payment_id, s1.payment, s1.date)
