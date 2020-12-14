from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.room import Room

from schemas.room import RoomSchema

room_schema = RoomSchema()
room_list_schema = RoomSchema(many=True)


class RoomListResource(Resource):

    def get(self):

        current_user = get_jwt_identity()

        all_rooms = Room.get_all_rooms()

# -- Tämä if lauseke tällähtekellä turha kun ei onnistu vain käyttäjän idn tarkistaminen jwt_identityn avulla.
# -- !! Huoneen päivittämisessä toimii käyttäjän idllä muokkauksen esto, TUTKI ASIAA !! --
# -- Nyt get rooms palauttaa kaikki huoneet oli ne listattu tai ei .. Täytyy itse lukea json:ista onko listed True vai False

        if current_user != 1:
            return room_list_schema.dump(all_rooms).data, HTTPStatus.OK

        rooms = Room.get_all_listed()

        return room_list_schema.dump(rooms).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()
        current_user = get_jwt_identity()

        data, errors = room_schema.load(data=json_data)

        
        if current_user != 1:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST

        room = Room(**data)
        room.user_id = 1
        room.save()

        return room_schema.dump(room).data, HTTPStatus.CREATED


class RoomResource(Resource):

    @jwt_optional
    def get(self, room_id):

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND

        return room_schema.dump(room), HTTPStatus.OK

    @jwt_required
    def put(self, room_id):

        json_data = request.get_json()

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != 1:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        room.name = json_data['name']
        room.description = json_data['description']
        room.location = json_data['location']

        room.save()

        return room_schema.dump(room), HTTPStatus.OK

    @jwt_required
    def patch(self, room_id):

        json_data = request.get_json()

        data, errors = room_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': 'Room not found'}, HTTPStatus.FORBIDDEN

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'mesage': 'Room not found'}, HTTPStatus.NOT_FOUND


        room.name = data.get('name') or room.name

        room.save()

        return room_schema.dump(room).data, HTTPStatus.OK


    @jwt_required
    def delete(self, room_id):

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != 1:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        room.delete()

        return {}, HTTPStatus.NO_CONTENT


class RoomListedResource(Resource):

    def put(self, room_id):
        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'room not found'}, HTTPStatus.NOT_FOUND

        room.is_listed = True
        room.save()

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, room_id):
        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'room not found'}, HTTPStatus.NOT_FOUND

        room.is_listed = False
        room.save()

        return {}, HTTPStatus.NO_CONTENT