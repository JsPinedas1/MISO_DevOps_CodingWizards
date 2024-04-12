from marshmallow import Schema, fields
from sqlalchemy import Column, String, DateTime
from .model import Model
from ..configDataBase import Base
from datetime import datetime

class Base(Model, Base):
	__tablename__ = "tbl_lista_negra"
	email = Column(String)
	appUuid = Column(String)
	blockedReason = Column(String)

	def __init__(self, email, appUuid, blockedReason):
		Model.__init__(self)
		self.email = email
		self.appUuid = appUuid
		self.blockedReason = blockedReason

class BaseSchema(Schema):
	id  = fields.UUID()
	email = fields.Str()
	appUuid = fields.Str()
	blockedReason = fields.Str()
	createdAt = fields.DateTime()
