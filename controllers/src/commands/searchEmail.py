from .. import configDataBase
from .baseCommand import BaseCommand
from ..errors.errors import EmailNotExist, TokenEmpty, TokenNoValid
from ..models.base import Base

import os

configDataBase.init()

class SearchEmail(BaseCommand):
  def __init__(self, email=None, token=None, check_db=True) -> None:
    super().__init__()
    if configDataBase.db_no_exist and check_db:
      configDataBase.init_db()
      configDataBase.create_table()
      configDataBase.db_no_exist = True
    
    self.email = email
    self.token = token
    self.realToken = os.getenv("TOKEN", "EQcfdZ[AUAY=qv/xtF.dVh-TL_0z")

  def execute(self):
    self.validateToken(self.token)
      
    db = configDataBase.db_manager.session()

    dataEmail = db.query(Base).filter(Base.email == self.email).first()
    if dataEmail is None:
      raise EmailNotExist
    
    return {
      "existe": True,
      "motivo": dataEmail.blockedReason,
    }

  def validateToken(self, token):    
    if token is None or not token:
      raise TokenEmpty
    if str(token) != str(self.realToken):
      raise TokenNoValid
