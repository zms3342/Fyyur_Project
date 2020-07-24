#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
import os
import sys
from flask_wtf import Form
from forms import *
from models import Venue, Artist, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# class Venue(db.Model):

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     genres=db.Column(db.ARRAY(db.String), nullable=False)
#     address = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     website=db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     currently_seeking=db.Column(db.Boolean, default=False, nullable=False)
#     seeking_message=db.Column(db.String(120))
#     shows =db.relationship("Show", backref="venue", lazy=True)


# class Artist(db.Model):

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     genres = db.Column(db.ARRAY(db.String), nullable=False)
#     website=db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     currently_seeking=db.Column(db.Boolean, default=False, nullable=False)
#     seeking_message=db.Column(db.String(120))
#     shows =db.relationship("Show", backref="artist", lazy=True)

#     # TODO: implement any missing fields, as a database migration using Flask-Migrate

# # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# class Show(db.Model): 
#   id=db.Column(db.Integer,primary_key=True)
#   venue_id=db.Column(db.Integer,db.ForeignKey('venue.id'), nullable=False)
#   artist_id=db.Column(db.Integer,db.ForeignKey('artist.id'), nullable=False)
#   datetime = db.Column(db.DateTime)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data1=[]
  # tuple (city, state)
  state_city = db.session.query(Venue.state, Venue.city).all()
  for state, city in state_city:
    instance1={}
    instance1["city"]=city
    instance1["state"]=state
    vens=[]
    for venue in db.session.query(Venue).filter_by(city=city, state=state).all():
      vens.append({"id":venue.id, "name":venue.name,})
    instance1["venues"]=vens
    data1.append(instance1)
  return render_template('pages/venues.html', areas=data1);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term')
  results = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all()

  response = {}
  response['count'] = len(results)
  response['data'] = results
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id]
  venue =Venue.query.get(venue_id)
  data=venue.details_full()
  data["past_shows"]=[]
  data["upcoming_shows"]=[]
  shows=db.session.query(Show).join(Venue).all()
  print(shows)
  upcoming_shows_count=0
  past_shows_count=0
  for show in shows: 
    artist_id=show.artist_id
    artist_name = Artist.query.get(artist_id).name
    artist_image_link= Artist.query.get(artist_id).image_link
    if show.datetime < datetime.today():
      past_shows_count+=1
      time= str(show.datetime)
      data['past_shows'].append({"artist_id":artist_id, "artist_name":artist_name, "artist_image_link": artist_image_link, "start_time":time})
    else: 
      upcoming_shows_count+=1
      time= str(show.datetime)
      data['upcoming_shows'].append({"artist_id":artist_id, "artist_name":artist_name, "artist_image_link": artist_image_link, "start_time":time})
  data["upcoming_shows_count"]=upcoming_shows_count
  data ["past_shows_count"]= past_shows_count
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try: 
    new_venue = Venue(
      name=request.form['name'],
      genres=request.form.getlist('genres'),
      city=request.form['city'],
      state=request.form['state'],
      address=request.form['address'],
      phone=request.form['address'],
      website=request.form['website'],
      facebook_link=request.form['facebook_link'],
      image_link=request.form['image_link'])
    db.session.add(new_venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data=[]
  info = db.session.query(Artist.id, Artist.name).all()
  for id, name in info: 
      data.append({"id":id,"name":name})
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term')
  results = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()

  response = {}
  response['count'] = len(results)
  response['data'] = results

  return render_template('pages/search_artists.html',results=response,search_term=request.form.get('search_term', ''))
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist =Artist.query.get(artist_id)
  data = artist.details_full()
  data["past_shows"]=[]
  data["upcoming_shows"]=[]
  shows=shows=db.session.query(Show).join(Artist).all()
  upcoming_shows_count=0
  past_shows_count=0
  for show in shows: 
    venue_id=show.artist_id
    venue_name = Venue.query.get(venue_id).name
    venue_image_link= Venue.query.get(venue_id).image_link
    if show.datetime < datetime.today():
      past_shows_count+=1
      time= str(show.datetime)
      data['past_shows'].append({"venue_id":venue_id, "venue_name":venue_name, "venue_image_link": venue_image_link, "start_time":time})
    else: 
      upcoming_shows_count+=1
      time= str(show.datetime)
      data['upcoming_shows'].append({"venue_id":venue_id, "venue_name":venue_name, "venue_image_link": venue_image_link, "start_time":time})
  data["upcoming_shows_count"]=upcoming_shows_count
  data ["past_shows_count"]= past_shows_count

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try: 
    edited = Artist.query.get(artist_id)
    fr=request.form
    edited.name = fr['name']
    edited.city = fr['city']
    edited.state= fr['state']
    edited.phone = fr['phone']
    edited.genres =fr.getlist('genres')
    edited.website=fr['website']
    edited.image_link=fr['image_link']
    edited.facebook_link=fr['facebook_link']
    edited.seeking_message=fr['seeking_message']
    if fr['currently_seeking']=='y': 
      edited.currently_seeking=True
    else: 
      edited.currently_seeking=False
    db.session.add(edited)
    db.session.commit()
    flash("successfully edited")
  except: 
        db.session.rollback()
        print(sys.exc_info())
        flash("something went wrong")
  finally: 
    db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try: 
    edited = Venue.query.get(venue_id)
    fr=request.form
    edited.name = fr['name']
    edited.city = fr['city']
    edited.state= fr['state']
    edited.phone = fr['phone']
    edited.genres =fr.getlist('genres')
    edited.website=fr['website']
    edited.image_link=fr['image_link']
    edited.facebook_link=fr['facebook_link']
    edited.seeking_message=fr['seeking_message']
    if fr['currently_seeking']=='y': 
      edited.currently_seeking=True
    else: 
      edited.currently_seeking=False
    db.session.add(edited)
    db.session.commit()
    flash("successfully edited")
  except: 
        db.session.rollback()
        print(sys.exc_info())
        flash("something went wrong")
  finally: 
    db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  artist_data = request.form
  try:
    new_artist=Artist(
      name= artist_data['name'],
      genres=artist_data.getlist('genres'),
      city=artist_data['city'],
      state=artist_data['state'],
      phone=artist_data['phone'],
      website=artist_data['website'],
      facebook_link=artist_data['facebook_link'],
      image_link=artist_data['image_link'])
    db.session.add(new_artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except: 
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

  finally:
    db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data=[]
  shows = db.session.query(Show.venue_id,Show.artist_id, Show.datetime).all()
  for venue,artist,datetime in shows: 
    venue_name=Venue.query.get(venue).name
    artist_name=Artist.query.get(artist).name
    artist_image_link=Artist.query.get(artist).image_link
    data.append({
      "venue_id":venue,
      "venue_name":venue_name,
      "artist_id":artist,
      "artist_name":artist_name,
      "artist_image_link":artist_image_link, 
      "start_time": str(datetime)})
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  show_item=request.form
  try:
    show = Show(
      artist_id=show_item['artist_id'],
      venue_id = show_item['venue_id'],
      datetime=show_item['datetime'])
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('oh no something didnt work')

  finally:
    db.session.close()
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
