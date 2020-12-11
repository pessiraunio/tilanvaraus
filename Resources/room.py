from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.rooms import room

from schemas.room import RoomSchema

room_schema = RoomSchema()
room_list_schema = RoomSchema(many=True)


class RoomListResource(Resource):

    def get(self):

        rooms = room.get_all_published()

        return room_list_schema.dump(rooms).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()
        current_user = get_jwt_identity()

        data, errors = room_schema.load(data=json_data)

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST

        room = room(**data)
        room.user_id = current_user
        room.save()

        return room_schema.dump(room).data, HTTPStatus.CREATED


class RoomResource(Resource):

    @jwt_optional
    def get(self, room_id):

        room = room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if room.is_publish == False and room.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return room.data(), HTTPStatus.OK

    @jwt_required
    def put(self, room_id):

        json_data = request.get_json()

        room = room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != room.user_id:
            return {'message': 'Acces is not allowed'}, HTTPStatus.FORBIDDEN

        room.name = json_data['name']
        room.description = json_data['description']
        room.steps = json_data['steps']
        room.tools = json_data['tools']
        room.cost = json_data['cost']
        room.duration = json_data['duration']

        room.save()

        return room.data(), HTTPStatus.OK

    @jwt_required
    def patch(self, room_id):

        json_data = request.get_json()

        data, errors = room_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': 'Room not found'}, HTTPStatus.FORBIDDEN

        room = room.get_by_id(room_id=room_id)

        if room is None:
            return {'mesage': 'Room not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != room.user_id:
            return {'message': 'Access not allowed'}, HTTPStatus.FORBIDDEN

        room.name = data.get('name') or room.name
        room.description = data.get('description') or room.description
        room.steps = data.get('steps') or room.steps
        room.tools = data.get('tools') or room.tools
        room.cost = data.get('cost') or room.cost
        room.duration = data.get('duration') or room.duration
        room.save()

        return room_schema.dump(room).data, HTTPStatus.OK

    @jwt_required
    def delete(self, room_id):

        room = room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != room.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        room.delete()

        return {}, HTTPStatus.NO_CONTENT


class RoomPublishResource(Resource):

    def put(self, room_id):
        room = room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND

        room.is_publish = True
        room.save()

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, room_id):
        room = room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found'}, HTTPStatus.NOT_FOUND

        room.is_publish = False

        return {}, HTTPStatus.NO_CONTENT