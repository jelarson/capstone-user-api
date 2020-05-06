from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from environs import Env
# from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt
# import bcrypt
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)
heroku = Heroku(app)
 
env = Env()
env.read_env()
DATABASE_URL = env("DATABASE_URL")

# test

basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#     os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Create ASL Table
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    loggedIn = db.Column(db.String(20), nullable=False)
    testOneHighScore = db.Column(db.String(20), nullable=False)
    testOnePassed = db.Column(db.String(20), nullable=False)
    testTwoHighScore = db.Column(db.String(20), nullable=False)
    testTwoPassed = db.Column(db.String(20), nullable=False)
    testThreeHighScore = db.Column(db.String(20), nullable=False)
    testThreePassed = db.Column(db.String(20), nullable=False)


    def __init__(self, name, email, password, loggedIn, testOneHighScore, testOnePassed, testTwoHighScore, testTwoPassed, testThreeHighScore, testThreePassed):
        self.name = name
        self.email = email
        # self.password = bcrypt.hashpw(password, bcrypt.gensalt())
        # self.password = password
        self.loggedIn = loggedIn
        self.testOneHighScore = testOneHighScore
        self.testOnePassed = testOnePassed
        self.testTwoHighScore = testTwoHighScore
        self.testTwoPassed = testTwoPassed
        self.testThreeHighScore = testThreeHighScore
        self.testThreePassed = testThreePassed
        self.password = bcrypt.generate_password_hash(password).decode(‘utf-8’)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'loggedIn', 'testOneHighScore', 'testOnePassed', 'testTwoHighScore', 'testTwoPassed', 'testThreeHighScore', 'testThreePassed')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/', methods=["GET"])
def home():
    return "<h1>USER API</h1>"

@app.route('/auth', methods=['POST'])
def auth_user():
  entered_password = request.json['entered_password']
  checked_password = request.json['checked_password']

  return str(bcrypt.check_password_hash(checked_password, entered_password))

@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password'] #hash?
    loggedIn = request.json['loggedIn']
    testOneHighScore = request.json['testOneHighScore']
    testOnePassed = request.json['testOnePassed']
    testTwoHighScore = request.json['testTwoHighScore']
    testTwoPassed = request.json['testTwoPassed']
    testThreeHighScore = request.json['testThreeHighScore']
    testThreePassed = request.json['testThreePassed']


    new_user = User(name, email, password, loggedIn, testOneHighScore, testOnePassed, testTwoHighScore, testTwoPassed, testThreeHighScore, testThreePassed)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)
    return user_schema.jsonify(user)


@app.route('/users', methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result)


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)

    result = user_schema.dump(user)
    return jsonify(result)


@app.route('/user/<id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get(id)

    new_loggedIn = request.json['loggedIn']
    new_testOneHighScore = request.json['testOneHighScore']
    new_testOnePassed = request.json['testOnePassed']
    new_testTwoHighScore = request.json['testTwoHighScore']
    new_testTwoPassed = request.json['testTwoPassed']
    new_testThreeHighScore = request.json['testThreeHighScore']
    new_testThreePassed = request.json['testThreePassed']

    user.loggedIn = new_loggedIn
    user.testOneHighScore = new_testOneHighScore
    user.testOnePassed = new_testOnePassed
    user.testTwoHighScore = new_testTwoHighScore
    user.testTwoPassed = new_testTwoPassed
    user.testThreeHighScore = new_testThreeHighScore
    user.testThreePassed = new_testThreePassed

    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    record = User.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Item deleted')

# POST request to validate password?



if __name__ == "__main__":
    app.debug = True
    app.run()


# password = b'hello'
# password2 = b'goodbye'

# hashed = bcrypt.hashpw(password, bcrypt.gensalt())
# hashed2 = bcrypt.hashpw(password2, bcrypt.gensalt())

# if bcrypt.checkpw(password, hashed):
#   print('match')
# else:
#   print('no match')

# print(hashed)
# print(hashed2)
