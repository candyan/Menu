 #-*- coding: UTF-8 -*-
import datetime

from flask import Flask, request, session
from flask import render_template

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babelex import Babel

from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.form import rules

from wtforms.fields import SelectField

from consts import DEPARTMENT_LIST, WEEK_NAMES

app = Flask(__name__)  # 实现一个Flask类的实例
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/cherry'  # 设置连接数据库地址
app.config['SECRET_KEY'] = '123456790'
db = SQLAlchemy(app)  # 实现SQLAlchemy 类的实例
app.debug = True  # 开启调试模式

babel = Babel(app)


@babel.localeselector
def get_locale():
    override = request.args.get('lang')

    if override:
        session['lang'] = override

    return session.get('lang', 'zh')


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64), unique=True)
    menu_str = db.Column(db.String(128))


class OrderMeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    name = db.Column(db.String(64))
    department = db.Column(db.String(128))


class OrderMealView(ModelView):
    column_labels = dict(create_time=u'订餐日期', name=u'姓名', department=u'部门')
    column_formatters = dict(create_time=lambda v, c, m, ct: m.create_time.strftime('%Y-%m-%d %A').decode('utf-8'))

    form_overrides = dict(department=SelectField)
    form_args = dict(
        department = dict(
            choices = [(department_name, department_name) for department_name in DEPARTMENT_LIST],
        )
    )

    form_create_rules = [
        'name',
        'department'
    ]

    can_edit = False

    def __init__(self, session, **kwargs):
        super(OrderMealView, self).__init__(OrderMeal, session, **kwargs)


class MenuView(ModelView):
    column_labels = dict(date=u'日期', menu_str=u'菜单')
    form_overrides = dict(date=SelectField)

    form_args = dict(
        date = dict(
            choices = [(WEEK_NAMES[index], WEEK_NAMES[index]) for index in range(len(WEEK_NAMES))],
        )
    )

    def __init__(self, session, **kwargs):
        super(MenuView, self).__init__(Menu, session, **kwargs)


@app.route('/')  # 路由
@app.route('/reserve/')
def index():
    menu = Menu.query.filter_by(date=get_today_weekname()).first()
    today_menu = menu.menu_str if menu else u'暂无菜单'
    return render_template('book.html', date=get_today_str(), menu=today_menu, department_list=DEPARTMENT_LIST)


@app.route('/all/')
def all_menus():
    menu_list = Menu.query.filter_by()
    dict = {}
    for item in menu_list:
        dict[item.date] = item.menu_str
    menu_content_list = []

    for name in WEEK_NAMES:
        if dict.has_key(name):
            menu_content = '%s: %s' % (name, dict[name])
            menu_content_list.append(menu_content)
    return render_template('all_menus.html', menu_list=menu_content_list)


@app.route('/order/all')
def all_order():
     order_list = OrderMeal.query.filter_by(date=get_today_str())
     order_dict = {}
     for item in order_list:
         if order_dict.has_key(item.department):
             order_dict[item.department].append(item.name)
         else:
             order_dict[item.department] = [item.name]
     return render_template('all_order.html', order_dict=order_dict)


@app.route('/order/add', methods=['POST', 'GET'])
def add_order():
    name = request.json["name"]
    department = request.json["department"]
    order_meal = OrderMeal(name=name, department=department)
    db.session.add(order_meal)
    db.session.commit()
    return "{}"


def get_today_weekname():
    today = datetime.date.today()
    return WEEK_NAMES[today.weekday()]


def get_today_str():
    today = datetime.date.today()
    ISOFORMAT = '%Y 年 %m 月 %d 日'
    return today.strftime(ISOFORMAT).decode('utf-8') + " " + get_today_weekname()


if __name__ == '__main__':
    admin = Admin(app, u'订餐后台')

    #admin.locale_selector(get_locale)

    admin.add_view(MenuView(db.session, name=u'菜单'))
    admin.add_view(OrderMealView(db.session, name=u'订餐信息'))

    db.create_all()
    app.run('0.0.0.0', 8000)

