from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from .models import Project, ProjectTask, MyMetrics, Doctype, MetricSlug

"""
    Create your Views (but don't register them here, do it on the manager::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)

    
"""
class ProjectTaskView(ModelView):
    datamodel = SQLAInterface(ProjectTask)
    list_columns = ['id','name']

class MetricsView(ModelView):
    datamodel = SQLAInterface(MyMetrics)

class DoctypeView(ModelView):
    datamodel = SQLAInterface(Doctype)

class MetricSlugView(ModelView):
    datamodel = SQLAInterface(MetricSlug)

class ProjectView(ModelView):
    datamodel = SQLAInterface(Project)
    list_columns = ['id', 'name', 'estimated_start_date','status']
    show_columns = ['id', 'name', 'estimated_start_date']
    edit_columns = ['id', 'name', 'estimated_start_date']

    related_views = [MetricsView, MetricSlugView]


    

