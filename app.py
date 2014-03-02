 #-*- coding: UTF-8 -*-
import datetime

from flask import Flask
from flask import render_template

from flask.ext.admin import Admin, BaseView, expose
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext import login

app = Flask(__name__) #实现一个Flask类的实例
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/cherry' #设置连接数据库地址
app.config['SECRET_KEY'] = '123456790'  
db = SQLAlchemy(app) #实现SQLAlchemy 类的实例
app.debug = True  #开启调试模式

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64), unique=True)
    menu_str = db.Column(db.String(128))

    def __unicode__(self):
        return 'hello'

class MenuView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

@app.route('/') #路由
@app.route('/reserve/')
def index():
    '''定义方法'''
    today_menu = Menu.query.filter_by(date=get_today_weekname()).first().menu_str
    return render_template('book.html', date=get_today_str(), menu=today_menu)

def get_today_weekname():
    today = datetime.date.today()
    week_list = u'星期一 星期二 星期三 星期四 星期五 星期六 星期日'.split()
    return week_list[today.weekday()]
    
def get_today_str():
    today = datetime.date.today()
    ISOFORMAT = '%Y 年 %m 月 %d 日'
    return today.strftime(ISOFORMAT).decode('utf-8') + " " + get_today_weekname()

if __name__ == '__main__':
    admin = Admin(app)
    admin.add_view(ModelView(Menu, db.session, name=u'菜单'))

    db.create_all()
    app.run('0.0.0.0', 8000)
