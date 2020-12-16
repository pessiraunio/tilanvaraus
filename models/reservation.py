from extensions import db
from models.user import User


#Että tää tuli näkyviin databaseen piti env.py tiedostoon piti lisätä "from models import reservation, room, user"

class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime(), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    is_listed = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    room = db.Column(db.String(), nullable=False)

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def data(self):
        return {
            'id': self.id, 
            'name': self.name, 
            'description': self.description,
            'date': self.date.strftime("%d/%m/%y"), 
            'time': self.time,
            'user': User.get_by_id(self.user_id).username, 
            'room': self.room
            }

    #roomreservation_id = db.Column(db.Integer(), db.ForeignKey("room.id"))
    #Linkataan reservatio > user settikeijo Tino tekee


    @classmethod
    def get_by_listed(cls):
        return cls.query.filter_by(is_listed=True).all()

    @classmethod
    def get_by_date_time_room(cls, date, time, room):
        return cls.query.filter_by(date=date, time=time, room=room).first()

    @classmethod
    def get_by_date_room(cls, date, room):
        return cls.query.filter_by(date=date, room=room).all()

    @classmethod
    def get_by_date(cls, date):
        return cls.query.filter_by(date=date).all()

    @classmethod
    def get_by_id(cls, reservation_id):
        return cls.query.filter_by(id=reservation_id).first()

    @classmethod
    def get_by_room(cls, room):
        return cls.query.filter_by(room=room).all()
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

