from sqlalchemy import Column, String

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key = True, index=True)
    key = Column(String, unique = False, index = True)
    session = Column(String, unique=False, index=True)
    mint = Column(String, unique = False, index = True)