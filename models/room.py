from extensions import db

class Room(db.Model):

    __tablename__ =  'room'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    reserver_id = db.Column(db.Integer, db.ForeignKey('user.id'))