from .. import configDataBase
from .baseCommand import BaseCommand
from ..errors.errors import EmailAlreadyExist, InvalidUuidFormat, RequestFieldEmpty, RequestFieldNotString, TokenEmpty, TokenNoValid
from ..models.base import Base

import os
import pytz
import re
import sys

utc=pytz.UTC
configDataBase.init()

class CreateEmail(BaseCommand):
  def __init__(self, email, appUuid, blockedReason, token) -> None:
    super().__init__()
    if configDataBase.db_no_exist:
      configDataBase.init_db()
      configDataBase.create_table()
      configDataBase.db_no_exist = True
    
    self.email = email
    self.appUuid = appUuid
    self.blockedReason = blockedReason
    self.token = token
    self.realToken = os.getenv("TOKEN", "EQcfdZ[AUAY=qv/xtF.dVh-TL_0z")

  def execute(self):
    self.validateToken(self.token)
    self.isEmptyNone(self.email)
    self.isEmptyNone(self.appUuid)
    self.isEmptyNone(self.blockedReason)
    
    print("email", self.email, file=sys.stderr)
    print("appUuid", self.appUuid, file=sys.stderr)
    print("blockedReason", self.blockedReason, file=sys.stderr)
    
    if not self.isUuidString(self.appUuid):
      raise InvalidUuidFormat

    db = configDataBase.db_manager.session()
    
    existingEmail = db.query(Base).filter(Base.email == self.email).first()
    if existingEmail is not None:
      raise EmailAlreadyExist
    
    newEmail = Base(
      email=self.email,
      appUuid=self.appUuid,
      blockedReason=self.blockedReason
    )
    db.add(newEmail)
    db.commit()
    return { "msg": "Se agreg\u00f3 el correo a la lista negra de la organizaci\u00f3n" }

  def isUuidString(self, appUuid):
    uuidRgex = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    return bool(uuidRgex.match(appUuid))
  
  def isEmptyNone(self, field):
    if field is None or not field:
      raise RequestFieldEmpty
    if type(field) != str:
      raise RequestFieldNotString

  def validateToken(self, token):    
    if token is None or not token:
      raise TokenEmpty
    if str(token) != str(self.realToken):
      raise TokenNoValid