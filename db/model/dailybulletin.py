from sqlalchemy import Column, Integer, SmallInteger, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DailyBulletinContracts(Base):
    __tablename__ = 'dailybulletin_contracts'
    # Column
    contract = Column(String(5), primary_key=True)
    expiration = Column(String(5))
    expiration_date = Column(Date)


class DailyBulletinReports(Base):
    __tablename__ = 'dailybulletin_reports'
    # Column
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    date = Column(String)
    index = Column(Integer)
    path = Column(String(255))
    status = Column(String(16), ForeignKey('dailybulletin_reports_status.status'))
    # Define the relationship
    status_obj = relationship("DailyBulletinReportsStatus", backref="reports")


class DailyBulletinReportsData:
    __tablename__ = 'dailybulletin_reports_data'
    # Column
    report_id = Column(Integer, ForeignKey('dailybulletin_reports_data.id'))
    section = Column(String(8), ForeignKey('dailybulletin_sections.section'))
    contract = Column(String(5), ForeignKey('dailybulletin_contracts.contract'))
    product = Column(SmallInteger, ForeignKey('dailybulletin_products.id'))


class DailyBulletinProducts:
    __tablename__ = 'dailybulletin_products'
    # Column
    id = Column(SmallInteger, primary_key=True)
    clearing = Column(String(4))
    globex = Column(String(4))
    floor = Column(String(4))
    clearport = Column(String(4))
    name = Column(String(64))
    exchange = Column(String(4))
    group = Column(String(16))
    sub_group = Column(String(16))
    category = Column(String(16))
    sub_category = Column(String(16))
    cleared_as = Column(String(16))


class DailyBulletinReportsStatus(Base):
    __tablename__ = 'dailybulletin_reports_status'

    status = Column(String(16), primary_key=True)


class DailyBulletinSections(Base):
    __tablename__ = 'dailybulletin_sections'
    # Column
    section = Column(String(8), primary_key=True)
    type = Column(String(8), ForeignKey('dailybulletin_sections_types.type'))
    # Relationships
    type_obj = relationship("DailyBulletinSectionsTypes", backref="sections")
    names = relationship("DailyBulletinSectionsNames", backref="section_obj", cascade="all, delete-orphan")
    subsections = relationship("DailyBulletinSectionsSubsections", backref="section_obj", cascade="all, delete-orphan")


class DailyBulletinSectionsNames(Base):
    __tablename__ = 'dailybulletin_sections_names'
    # Column
    section = Column(String(8), ForeignKey('dailybulletin_sections.section'), primary_key=True)
    seq = Column(Integer, primary_key=True)
    name = Column(String(255))


class DailyBulletinSectionsSubsections(Base):
    __tablename__ = 'dailybulletin_sections_subsections'
    # Column
    section = Column(String(8), ForeignKey('dailybulletin_sections.section'), primary_key=True)
    seq = Column(Integer, primary_key=True)
    name = Column(String(255))


class DailyBulletinSectionsTypes(Base):
    __tablename__ = 'dailybulletin_sections_types'
    # Column
    type = Column(String(8), primary_key=True)
