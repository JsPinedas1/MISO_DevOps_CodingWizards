import os
import sys
from dataclasses import dataclass
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Optional, AsyncGenerator
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import ProgrammingError, OperationalError
from sqlalchemy.orm import sessionmaker, scoped_session

class Base(DeclarativeBase):
  pass 

class SingletonDBManager(type):
  _instances = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super().__call__(*args, **kwargs)
    return cls._instances[cls]

@dataclass
class DataBaseManager(metaclass=SingletonDBManager):
  DATABASE_USERNAME: Optional[str] = os.getenv("DB_USER", "postgres")
  DATABASE_PASSWORD: Optional[str] = os.getenv("DB_PASSWORD", "postgres")
  DATABASE_URI: Optional[str] = os.getenv("DB_HOST")
  DATABASE_PORT: Optional[str] = int(os.getenv("DB_PORT", "5432"))
  DATABASE_NAME: Optional[str] = os.getenv("DB_NAME", "postgres")
  POOL_SIZE: int = 20
  MAX_OVERFLOW: int = 5
  POOL_RECYCLE: int = 60

  def __init__(self):
    self._engine = None
    self._sync_engine = None
    self._async_engine = None

  def __enter__(self):
    self._session = self.session()
    return self._session

  async def __aenter__(self):
    self._async_session = await self.async_session()
    return self._async_session

  def __exit__(self, exc_type, exc_val, exc_tb):
    self._session.close()

  async def __aexit__(self, exc_type, exc_val, exc_tb):
    await self._async_session.close()

  def sync_engine(self):
    try:
      print("****** VARIABLES ******")
      print("DATABASE_USERNAME", self.DATABASE_USERNAME)
      print("DATABASE_PASSWORD", self.DATABASE_PASSWORD)
      print("DATABASE_URI", self.DATABASE_URI)
      print("DATABASE_PORT", self.DATABASE_PORT)
      print("DATABASE_NAME", self.DATABASE_NAME)
      print("***********************")
      if self._engine is None:
        self._engine = create_engine(
          f"postgresql+psycopg2://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_URI}:"
          f"{self.DATABASE_PORT}/{self.DATABASE_NAME}",
          pool_size=self.POOL_SIZE,
          max_overflow=self.MAX_OVERFLOW,
          pool_recycle=self.POOL_RECYCLE,
          pool_timeout=10
        )
      return self._engine
    except Exception as e:
      raise Exception(f"Error creating sync engine: {e}") from e

  async def async_engine(self):
    try:
      if self._async_engine is None:
        self._async_engine = create_async_engine(
          f"postgresql+asyncpg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_URI}:"
          f"{self.DATABASE_PORT}/{self.DATABASE_NAME}",
          future=True,
          pool_size=self.POOL_SIZE,
          max_overflow=self.MAX_OVERFLOW,
          pool_recycle=self.POOL_RECYCLE,
          pool_timeout=10,
          pool_pre_ping=True,
        )
      return self._async_engine
    except Exception as e:
      raise Exception(f"Error creating async engine: {e}") from e

  def session(self):
    return sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=self.sync_engine())()

  async def async_session(self):
    return scoped_session(sessionmaker(bind=await self.async_engine(), class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False))()

db_manager = DataBaseManager()

@asynccontextmanager
async def get_async_session():
  db = await db_manager.async_session()
  try:
    yield db
  finally:
    await db.close()

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
  async with get_async_session() as db:
    yield db

def init(value = True):
  global db_no_exist
  db_no_exist = value

def init_db():
  print("dropping the old test db…", file=sys.stderr)
  engine = db_manager.sync_engine()
  print("Created engine", file=sys.stderr)
  try:
    conn = engine.connect()
    print("Created connection to the engine..", file=sys.stderr)
    conn = conn.execution_options(autocommit=False)
    print("Setting up connection options...", file=sys.stderr)
    conn.execute(text("ROLLBACK"))
    conn.execute(text(f"DROP DATABASE {db_manager.DATABASE_NAME}"))
  except ProgrammingError:
    print("Could not drop the database, probably does not exist.", file=sys.stderr)
    conn.execute(text("ROLLBACK"))
    conn.execute(text(f"CREATE DATABASE {db_manager.DATABASE_NAME}"))
  except OperationalError:
    print("Could not drop database because it's being accessed by other users (psql prompt open?)", file=sys.stderr)
    conn.execute(text("ROLLBACK"))
  except Exception as error:
    print(f"ERROR FALTALISIMO 2: {error}")
  print(f"Test db dropped! about to create {db_manager.DATABASE_NAME}", file=sys.stderr)  
  try:
    conn.execute(text(f"create user {db_manager.DATABASE_USERNAME} with encrypted password '{db_manager.DATABASE_PASSWORD}'"))
  except:
    print("User already exists.", file=sys.stderr)
    conn.execute(text(f"grant all privileges on database {db_manager.DATABASE_NAME} to {db_manager.DATABASE_USERNAME}"))
  conn.close()
  print("Test db created", file=sys.stderr)

def create_table():
  Base.metadata.create_all(bind=db_manager.sync_engine())