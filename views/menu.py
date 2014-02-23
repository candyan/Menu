#-*- coding: UTF-8 -*-

from flask.ext.admin.contrib.sqla import ModelView

class MenuView(ModelView):
    # Disable model creation
    can_create = False

    # Override displayed fields
    column_list = ('日期', '菜单')

#    def __init__(self, session, **kwargs):
#        # You can pass name and other parameters if you want to
#        super(MyView, self).__init__(User, session, **kwargs)
