from extensions import db

class Room(db.Model):

    __tablename__ =  'room'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())



    @classmethod
    def get_all_rooms(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()


    #Tähän reservationista tablesta reservation idllä kaikki käyttäjän pöydät??  vai ei sitä ollenkaan.
    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()


