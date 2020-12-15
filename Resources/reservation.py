from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.room import Room
from models.reservation import Reservation

from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from datetime import datetime
from dateutil import parser


class ReservationListResource(Resource):
    def get(self):

        reservations = Reservation.get_by_listed()
        data = []

        for reservation in reservations:
            if not reservation.date < datetime.now():
                data.append(reservation.data())

        return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):

        def is_valid_date(year, month, day):
            day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                day_count_for_month[2] = 29
            return 1 <= month <= 12 and 1 <= day <= day_count_for_month[month]

        json_data = request.get_json()
        current_user = get_jwt_identity()

        if not Room.get_by_name(json_data['room']):
            return {'message': 'Room does not exist'}, HTTPStatus.BAD_REQUEST

        date_time_str = json_data['date']
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y')

        if not 15 < json_data['time'] < 21:
            return {'message': 'Only hours between 16-20 can be booked'}, HTTPStatus.BAD_REQUEST

        if date_time_obj < datetime.now():
            return {'message': 'Date already passed'}, HTTPStatus.BAD_REQUEST, print(date_time_obj)

        if not is_valid_date(date_time_obj.year, date_time_obj.month, date_time_obj.day):
            return {'not a real date'}, HTTPStatus.BAD_REQUEST

        if date_time_obj.weekday() > 5:
            return {'message': 'Room cant be reserved for the weekend'}, HTTPStatus.BAD_REQUEST

        if Reservation.get_by_date_time_room(date_time_obj, json_data['time'], json_data['room']):
            return {'message': 'Already booked'}, HTTPStatus.BAD_REQUEST

        reservation = Reservation(
        name=json_data['name'], 
        user_id=current_user, 
        room=json_data['room'],
        description=json_data['description'],
        date=date_time_obj,
        time=json_data['time'])

        reservation.save()
        return reservation.data(), HTTPStatus.CREATED


class ReservationResource(Resource):

    @jwt_required
    def put(self, reservation_id):

        json_data = request.get_json()

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.room_id = json_data['room_id']
        reservation.description = json_data['description']
        reservation.time = json_data['time']
        reservation.date = json_data['date']

        reservation.save()

        return reservation.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, reservation_id):

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.delete()

        return {}, HTTPStatus.NO_CONTENT

    def get(self, room, date):
        reservations = Reservation.get_by_date_room(date, room)
        data = []

        for reservation in reservations:
            data.append(reservation.data())

        return {'data': data}, HTTPStatus.OK
