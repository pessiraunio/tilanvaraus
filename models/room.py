from extensions import db

class Room(db.Model):

    __tablename__ =  'room'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(100))
    location = db.Column(db.String(100), nullable=False)
    is_listed = db.Column(db.Boolean(), default=True)

    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    

    @classmethod
    def get_all_listed(cls):
        return cls.query.filter_by(is_listed=True).all()
    
    @classmethod
    def get_all_rooms(cls):
        return cls.query.all()

    @classmethod
    def get_by_name(cls, room_name):
        return cls.query.filter_by(name=room_name).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    #Tähän reservationista tablesta reservation idllä kaikki käyttäjän pöydät??  vai ei sitä ollenkaan.
    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=roomreservation_id).all()

    @classmethod
    def get_by_id(cls, room_id):
        return cls.query.filter_by(id=room_id).first()


