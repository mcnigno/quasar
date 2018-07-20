from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn,
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Sequence, CHAR, Boolean, Text
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
    metrics = Column(CHAR(36), ForeignKey('metrics.id'))
    metric = relationship('Metrics')

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

class Metrics(Model, AuditMixin):
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Strig(50), nullable=False)
    description = Column(Text)
    active = Column(Boolean())
    value = Column(Integer())
    project_id = Column(CHAR(36), ForeignKey('project.id'))
    project = relationship('Project')
    doctype_id = Column(CHAR(36), ForeignKey('doctype.id'))
    doctype = relationship('Doctype')


class Doctype(Model, AuditMixin):
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Strig(50), nullable=False)
    description = Column(Text)

class MetricSlug(model, AuditMixin):
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Strig(50), nullable=False)
    doctype_id = Column(CHAR(36), ForeignKey('doctype.id'))
    doctype = relationship('Doctype')
    date = Column(Date, nullable=False)
    project_id = Column(CHAR(36), ForeignKey('project.id'))
    project = relationship('Project')







