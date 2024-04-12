from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Model():
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

  createdAt = Column(DateTime)

  def __init__(self):
    self.createdAt = datetime.now(tz=timezone.utc)