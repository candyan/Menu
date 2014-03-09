#-*- coding: UTF-8 -*-
from .app import db
from flask.ext.sqlalchemy import SQLAlchemy

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64), unique=True)
    menu_str = db.Column(db.String(128))

    def __unicode__(self):
        return 'hello'
