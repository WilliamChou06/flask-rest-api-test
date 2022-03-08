from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from db import db
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from flask_jwt_extended import create_access_token, JWTManager

app = Flask(__name__)
# To allow flask propagating exception even if debug is set to false on app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=30000000)
app.config['JWT_SECRET_KEY'] = 'william'
api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(User, '/users/<string:user_id>')
api.add_resource(UserRegister, '/signup')
api.add_resource(UserLogin, '/login')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True
