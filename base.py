#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:46:22 2021

@author: erikedmonds
"""
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#TODO: Add this back in
#from modules import get_coordinates

#Credentials
from EPA_credentials import TOKEN

import requests,json

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField('Please enter zip code', validators=[DataRequired()])
    limit = StringField('Enter charging station limit (default 10)')
    submit = SubmitField('Submit')

class Coordinate(object):
    def __init__(self,latitude,longitude):
        self.__latitude = latitude
        self.__longitude = longitude
        
    @property
    def latitude(self):
        return self.__latitude
    
    @property
    def longitude(self):
        return self.__longitude
# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    if form.validate_on_submit():
        zipcode = form.name.data
        limit = form.limit.data
        return redirect( url_for('location', zipcode=zipcode, limit=limit) )
    return render_template('index.html', form=form)

@app.route('/location/<zipcode>?limit=<limit>')
def location(zipcode,limit):
    # run function to get actor data based on the id in the path
    #zipcode = get_zipcode(zipcode)
    url=f'https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?location={zipcode}&fuel_type=ELEC&limit={eval(limit)+1}&api_key={TOKEN}'
    response = requests.get(url)
    
    #Insert assertion/error handling
    value=json.loads(response.text)
    
    #Change to accept multiple values
    stations=[Coordinate(fuel['latitude'],fuel['longitude']) for fuel in value['fuel_stations']]
    return render_template('location.html', 
                           center_latitude=stations[0].latitude,
                           center_longitude=stations[0].longitude,
                           data=[(point.latitude, point.longitude) for point in stations[1:]])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
