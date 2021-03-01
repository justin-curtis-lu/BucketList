from flask import Flask
from routes import main
from extensions import mongo
from key import mongoKey

app = Flask(__name__)

app.config['MONGO_URI'] = mongoKey

mongo.init_app(app)

app.register_blueprint(main)

if __name__ == "__main__":
    app.debug = True
    app.run()