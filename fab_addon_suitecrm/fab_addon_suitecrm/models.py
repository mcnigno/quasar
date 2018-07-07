from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
 
class Project(Model):
    __bind_key__ = 'suitecrm'
    id = Column(Integer, primary_key=True)
    name =  Column(String(50), nullable=False)