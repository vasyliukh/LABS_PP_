import pytest
from app import User,app,create_app,datetime,jwt

test = app.test_client()
@pytest.fixture()
def createapp():
    app = create_app()
    app.app_context().push()



@pytest.fixture()
def login_the_user():
    app = create_app()
    app.app_context().push()
    app.testing = True
    client = app.test_client()
    global token
    id = User.query.filter_by(username=username).first().id
    token = jwt.encode({'id': id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'])
    yield client
    app.testing = False

class TestCreateUser:

    def test1(self):
        data = {'login': 'Bodia', 'password': '1010', 'username': 'Bohdan'}
        test1 = test.post('/User', json=data)
        assert test1.status_code == 200
        assert test1.get_json() == [{'message': 'Invalid input'}, 400]

    def test2(self):
        data = {'login': 'Bodia', 'password': '22222222'}
        test2 = test.post('/User', json=data)
        assert test2.status_code == 200
        assert test2.get_json() == [{'message': 'Invalid input'}, 400]

    def test5(self, createapp):
        data = {'username':'user1',
              'firstName':'Olersandr',
              'lastName':'filiponov',
              'userStatus':'user',
              'email':'user@gmail.com',
              'password':'1649',
              'phone':'05641489' }
        global username
        username = data['username']
        test5 = test.post('/User', json=data)
        assert test5.status_code == 200
        assert User.query.filter_by(username=str(data['username'])).first() is not None



class TestLogin:
    def test1(self):
        test1 = test.get('/login', json=None)
        assert test1.status_code == 401

    def test2(self):
        data = {'username': 'NoUser', 'password': '22222222'}
        test2 = test.get('/login', json=data)
        assert test2.status_code == 401

    def test3(self):
        data = {'username': 'bodik', 'password': '12345678'}
        test3 = test.get('/login', json=data)
        assert test3.status_code == 401



class TestLogin:
    def test1(self):
        test1 = test.get('/login', json=None)
        assert test1.status_code == 401

    def test2(self):
        data = {'username': 'NoUser', 'password': '22222222'}
        test2 = test.get('/login', json=data)
        assert test2.status_code == 401

    def test3(self):
        data = {'username': 'bodik', 'password': '12345678'}
        test3 = test.get('/login', json=data)
        assert test3.status_code == 401

    def test4(self):
        data = {'username': 'bodik', 'password': '22222222'}
        test4 = test.get('/login', json=data)
        assert test4.status_code == 200


class TestEditUser:

    def test1(self, login_the_user):
        data = {'new_login': "super_hot_bodia"}
        headers = {'x-access-token': token}
        test1 = test.put('/UserUpdate', json=data, headers=headers)
        assert test1.status_code == 200
        assert test1.get_json() == [{"message": "User with this data already exist"}, 404]

    def test2(self, login_the_user):
        data = {'new_password': "12345678"}
        headers = {'x-access-token': token}
        test2 = test.put('/UserUpdate', json=data, headers=headers)
        assert test2.status_code == 200


    def test4(self, login_the_user):
        data = {'new_login': "Bohdan"}
        headers = {'x-access-token': token}
        test4 = test.put('/UserUpdate', json=data, headers=headers)
        assert test4.status_code == 200

    def test5(self, login_the_user):
        data = {'new_user_name': "Bohdan"}
        global username
        username = "Bohdan"
        headers = {'x-access-token': token}
        test5 = test.put('/UserUpdate', json=data, headers=headers)
        assert test5.status_code == 200