from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db
from resources.classroom import ClassroomResource, ClassroomListResource

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()
    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def register_resources(app):
    api = Api(app)

    api.add_resource(ClassroomResource, '/classrooms/<int:classroom_id>')
    api.add_resource(ClassroomListResource, '/classrooms')

if __name__ == '__main__':
    app = create_app()
    app.run(port=5050, debug=True)