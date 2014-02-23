 #-*- coding: UTF-8 -*-

from flask import Flask
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext import login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/cherry'
app.config['SECRET_KEY'] = '123456790'
db = SQLAlchemy(app)
app.debug = True

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64), unique=True)
    menu_str = db.Column(db.String(128))

    def __unicode__(self):
        return 'hello'

class MenuView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

if __name__ == '__main__':
    admin = Admin(app)
    admin.add_view(MenuView(Menu, db.session, name=u'菜单'))

    db.create_all()
    app.run('0.0.0.0', 8000)
