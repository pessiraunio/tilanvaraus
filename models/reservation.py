from extensions import db


class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    listed = db.Column(db.Boolean(), default=False)
    time = db.Column(db.DateTime(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    room_id = db.Column(db.Integer(), nullable=False)

    roomreservation_id = db.Column(db.Integer(), db.ForeignKey("room.id"))

    def data(self):
        return {'id': self.id, 'description': self.description, 'time': self.time, 'user_id': self.user_id,
                'room_id': self.room_id}


    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
