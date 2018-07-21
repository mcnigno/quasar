from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Sequence, CHAR, Boolean, Text
from sqlalchemy.orm import relationship

"""
class Project(Model):
    __bind_key__ = 'suitecrm'
    __table_args__ = {'info': dict(is_view=True)}
    __tablename__ = 'project'

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
    __table_args__ = {'info': dict(is_view=True)}

    id = Column(CHAR(36), primary_key=True, nullable=False)
    name =  Column(String(50), nullable=False)
    assigned_user_id = Column(String(38))
    status = Column(String(38))
    deleted = Column(String(38))
    project_id = Column(CHAR(36), ForeignKey('project.id'))
    project = relationship('Project')
    
    def __repr__(self):
        return self.name

class Doctype(Model, AuditMixin):
    __bind_key__ = 'crmext'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text)

    def __repr__(self):
        return self.name

class MyMetrics(Model, AuditMixin):
    __bind_key__ = 'crmext'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    active = Column(Boolean())
    value = Column(Integer())
    project_id = Column(CHAR(36), ForeignKey('project.id'))
    project = relationship('Project')
    doctype_id = Column(CHAR(36), ForeignKey('doctype.id'))
    doctype = relationship('Doctype')

    def __repr__(self):
        return self.name



class MetricSlug(Model, AuditMixin):
    __bind_key__ = 'crmext'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    doctype_id = Column(CHAR(36), ForeignKey('doctype.id'))
    doctype = relationship('Doctype')
    date = Column(Date, nullable=False)
    project_id = Column(CHAR(36), ForeignKey('project.id'))
    project = relationship('Project')

    def __repr__(self):
        return self.name

"""





