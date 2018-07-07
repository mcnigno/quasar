from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Sequence, CHAR
from sqlalchemy.orm import relationship
 
class Project(Model):
    __bind_key__ = 'suitecrm'
    id = Column(CHAR(36), primary_key=True, nullable=False)
    name =  Column(String(50), nullable=False)
    assigned_user_id = Column(String(38))
    estimated_start_date = Column(Date)
    estimated_end_date = Column(Date)
    status = Column(String(38))
    deleted = Column(String(38))

    def __repr__(self):
        return self.name

class ProjectTask(Model):
    __bind_key__ = 'suitecrm'
    id = Column(CHAR(36), primary_key=True, nullable=False)
    name =  Column(String(50), nullable=False)
    assigned_user_id = Column(String(38))
    status = Column(String(38))
    deleted = Column(String(38))
    project_id = Column(CHAR(36), ForeignKey('project.id'))
    project = relationship('Project')
