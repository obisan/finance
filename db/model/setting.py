from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Setting(Base):
    __tablename__ = 'setting'
    # Column
    id = Column(Integer, primary_key=True)
    param_name = Column(String)
    param_value = Column(String)
