  
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import datetime

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)



class Venue(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    genres=db.Column(db.ARRAY(db.String), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website=db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    currently_seeking=db.Column(db.Boolean, default=False, nullable=False)
    seeking_message=db.Column(db.String(120))
    shows =db.relationship("Show", backref="venue", lazy=True)

    def __init__(self, id, name, city, state, genres, address, phone, website, image_link, facebook_link, currently_seeking=False,seeking_message='' ):
        self.id= id
        self.name = name
        self.city = city
        self.state = state
        self,genres = genres
        self.address = address
        self.phone = phone 
        self.website = website
        self.image_link= image_link
        self.facebook_link = facebook_link
        self.currently_seeking= currently_seeking
        self.seeking_message = seeking_message

    def insert(self): 
        db.session.add(self)
        db.session.commit()

    def update(self): 
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def details_full(self):
        items = {
        "id":self.id,
        "name":self.name,
        "city": self.city,
        "state": self.state,
        "genres": self.genres,
        "address":self.address,
        "phone" : self.phone,
        "website":self.website,
        "image_link":self.image_link,
        "facebook_link":self.facebook_link,
        "currently_seeking":self.currently_seeking,
        "seeking_message": self.seeking_message,
        }
        return items
        

class Artist(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website=db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    currently_seeking=db.Column(db.Boolean, default=False, nullable=False)
    seeking_message=db.Column(db.String(120))
    shows =db.relationship("Show", backref="artist", lazy=True)

    def __init__(self, id, name, city, state, genres, address, phone, website, image_link, facebook_link, currently_seeking=False,seeking_message='' ):
        self.id= id
        self.name = name
        self.city = city
        self.state = state
        self.genres = genres
        self.phone = phone 
        self.website = website
        self.image_link= image_link
        self.facebook_link = facebook_link
        self.currently_seeking = currently_seeking
        self.seeking_message = seeking_message

    def insert(self): 
        db.session.add(self)
        db.session.commit()

    def update(self): 
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def details_full(self):
        items = {
        "id":self.id,
        "name":self.name,
        "city": self.city,
        "state": self.state,
        "genres": self.genres,
        "phone" : self.phone,
        "website":self.website,
        "image_link":self.image_link,
        "facebook_link":self.facebook_link,
        "currently_seeking":self.currently_seeking,
        "seeking_message": self.seeking_message,
        }
        return items


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model): 
    id=db.Column(db.Integer,primary_key=True)
    venue_id=db.Column(db.Integer,db.ForeignKey('venue.id'), nullable=False)
    artist_id=db.Column(db.Integer,db.ForeignKey('artist.id'), nullable=False)
    datetime = db.Column(db.DateTime)


    def __init__(self, id , venue_id, artist_id, datetime): 
        self.id = id
        self.venue_id = venue_id
        self.artist_id = artist_id
        self.datetime = datetime

    def insert(self): 
        db.session.add(self)
        db.session.commit()

    def update(self): 
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def details_full(self):
        items= {
        "id": self.id,
        "venue_id": self.venue_id, 
        "artist_id": self.artist_id,
        "datetime": self.datetime
        }



