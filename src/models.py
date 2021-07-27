from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    homeworld = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship ('Planet', lazy=True)
    people_favorites =  db.relationship ('Favoritespeople', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "homeworld": self.homeworld
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    density = db.Column(db.String(120), unique=True, nullable=False)
    gravity = db.Column(db.Integer)
            
    def __repr__(self):
        return 'Planet' + self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "density": self.density,
            "gravity": self.gravity
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id =  db.Column( db.Integer, primary_key=True)
    name =  db.Column( db.String(80), nullable=False)
    model =  db.Column( db.String(80), nullable=False)
    manufacturer =  db.Column( db.String(80), nullable=False)
    pilots = db.Column(db.Integer, db.ForeignKey('people.id'))
    user =  db.Column( db.String(80), nullable=False)
    
    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "pilots": self.pilots
        }

class Favoritespeople(db.Model):
    __tablename__ = 'favoritespeople'
    id = db.Column(db.Integer, primary_key=True)
    people = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    favorites = db.Column(db.Integer, db.ForeignKey('user.id'))
           
    def __repr__(self):
        return self.favorites_people

    def serialize(self):
        return {
            "id": self.id_fav,
            "people": self.people,
            "favorites":self.favorites
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    userfavorites =  db.relationship ('Favoritespeople', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
            # do not serialize the password, its a security breach
        }
