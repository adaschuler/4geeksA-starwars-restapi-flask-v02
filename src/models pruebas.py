from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    homeworld = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship ('Planet', lazy=True)
    people_favorites = db.relationship('Favoritespeople', backref="people", lazy=True)

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
    planet_favorites = db.relationship('Favoritesplanet', backref="planet", lazy=True)
            
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
    vehicles_favorites = db.relationship('Favoritesvehicles', backref="vehicles", lazy=True)
    
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

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('people'), nullable=False)
    favorito_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
           
    def __repr__(self):
        return self.id

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "people_name":self.people.name,
            "user_id":self.user_id
        }

class Favoritesplanet(db.Model):
    __tablename__ = 'favoritesplanet'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
           
    def __repr__(self):
        return self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "planet_name":self.planet.name,
            "user_id":self.user_id
        }

class Favoritesvehicles(db.Model):
    __tablename__ = 'favoritesvehicles'
    id = db.Column(db.Integer, primary_key=True)
    vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
           
    def __repr__(self):
        return self.id

    def serialize(self):
        return {
            "id": self.id,
            "vehicles_id": self.vehicles_id,
            "vehicles_name":self.vehicles.name,
            "user_id":self.user_id
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites_people = db.relationship('Favoritespeople', backref="user", lazy=True)
    favorites_planet = db.relationship('Favoritesplanet', backref="user", lazy=True)
    favorites_vehicles = db.relationship('Favoritesvehicles', backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favoritespeople": self.getFavoritesPeople(),
            "favoritesplanet": self.getFavoritesPlanet(),
            "favoritesvehicles": self.getFavoritesVehicles()
            # do not serialize the password, its a security breach
        }

    def getFavoritesPeople(self):
        return list(map(lambda fav: fav.serialize(),self.favorites_people))

    def getFavoritesPlanet(self):
        return list(map(lambda fav: fav.serialize(),self.favorites_planet))
    
    def getFavoritesVehicles(self):
        return list(map(lambda fav: fav.serialize(),self.favorites_vehicles))
