from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
import os
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_datepicker import datepicker

"""Tests for DB"""
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# app.config['SECRET_KEY'] = 'TEST'
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.cli.command()
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.route('/')
def index():
    # TODO Hier muss das aktuelle Event ausgewählt werden
    return render_template('index.html')

@app.route('/decision')
def decision():
    return render_template('decision.html')

@app.route('/decision-unclear')
def decisionUnclear():
    return render_template('decision-unclear.html')

@app.route('/event')
def event():
    return render_template('event.html')

@app.route('/create-HP')
def createHP():
    return render_template('create-HP.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/give-slugs')
def giveSlugs():
    return render_template('give-slugs.html')

@app.route('/invitation')
def invitation():
    return render_template('invitation.html')

@app.route('/invitation-accepted')
def invitationAccepted():
    return render_template('invitation-accepted.html')

if __name__ == '__main__':
    bootstrap = Bootstrap(app)
    bootstrap.run()
    datepicker(app)
    # app.run()
