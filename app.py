from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db
from extensions import jwt
from resources.user import User, UserListResource, UserResource, UserRoomListResource, MeResource
from resources.token import TokenResource, RefreshResource, RevokeResource
from resources.room import RoomListResource, RoomResource, RoomListedResource
from resources.reservation import ReservationListResource, ReservationResource, \
    ReservationRoomResource, ReservationDateResource



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list


def register_resources(app):
    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(UserRoomListResource, '/users/<string:username>/rooms')
    api.add_resource(MeResource, '/me')

    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')

    api.add_resource(RoomListResource, '/rooms')
    api.add_resource(RoomResource, '/rooms/<int:room_id>')
    api.add_resource(RoomListedResource, '/rooms/<int:room_id>/listed')

    api.add_resource(ReservationListResource, '/reservations')
    api.add_resource(ReservationResource, '/reservations/<int:reservation_id>')


    #T -- Lisäsin nämä
    api.add_resource(ReservationDateResource, '/reservations/date/<string:date_string>')
    api.add_resource(ReservationRoomResource, '/reservations/room/<string:room_name>')



    #api.add_resource(Reservation, /reservations/'huoneenimistring'/'aika string'2.3.2020,32:23.232313<)
    #lisätään näin ^^
if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    app.run(port=5050, debug=True)
