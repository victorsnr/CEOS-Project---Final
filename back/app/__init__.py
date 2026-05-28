from flask import Flask
from routes.web import web
from routes.users import api_users
from routes.tasks import api_tasks
from routes.auth import api_auth
from extensions import db, jwt

def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api_tasks, url_prefix = '/api')
    app.register_blueprint(api_users, url_prefix = '/api')
    app.register_blueprint(api_auth, url_prefix = '/api')
    app.register_blueprint(web)

    return app