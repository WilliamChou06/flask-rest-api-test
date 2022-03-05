from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
# To allow flask propagating exception even if debug is set to false on app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=30000000)
app.secret_key = 'william'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/signup')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
