from sqlalchemy import Column, SmallInteger, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UniqueGlobex(Base):
    __tablename__ = 'unique_globex'
    # Column
    globex = Column(String(4), primary_key=True)


class UniqueGlobexSymbol(Base):
    __tablename__ = 'unique_globex_symbol'
    # Column
    globex = Column(String(5), primary_key=True)


class DailyBulletinContracts(Base):
    __tablename__ = 'dailybulletin_contracts'
    # Column
    symbol = Column(String(5), ForeignKey('dictionary_symbol.symbol'), primary_key=True)
    year = Column(String(4), ForeignKey('dictionary_year.year'), primary_key=True)
    month = Column(String(1), ForeignKey('dailybulletin_report_contracts_symbol_month.month_literal'))
    product_group = Column(String(8))
    underlying = Column(String(4))
    first_avail = Column(Date)
    expiration = Column(DateTime(timezone=True))
    settle = Column(Date)
    clearing = Column(String(4))
    globex = Column(String(4))
    prs = Column(String(4))
    floor = Column(String(4))
    group = Column(String(4))
    itc = Column(String(4))
    exchange_contract = Column(String(4))
    type = Column(String(8))


class DailyBulletinReports(Base):
    __tablename__ = 'dailybulletin_reports'
    # Column
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    date = Column(Date)
    index = Column(Integer)
    path = Column(String(255))
    status = Column(String(16), ForeignKey('dailybulletin_reports_status.status'))
    # Define the relationship
    status_obj = relationship("DailyBulletinReportsStatus", backref="reports")


class DailyBulletinReportsData(Base):
    __tablename__ = 'dailybulletin_reports_data'
    # Column
    report_id = Column(Integer, ForeignKey('dailybulletin_reports.id'), primary_key=True)
    section = Column(String(8), ForeignKey('dailybulletin_sections.section'), primary_key=True)
    symbol = Column(String(5), ForeignKey('dictionary_symbol.symbol'), primary_key=True)
    year = Column(String(4), ForeignKey('dictionary_year.year'), primary_key=True)
    strike = Column(String(8), primary_key=True)
    strike_index = Column(SmallInteger, primary_key=True)
    type = Column(String(8), ForeignKey('dailybulletin_sections_types.type'))
    open_range = Column(String(8))
    high = Column(String(8))
    low = Column(String(8))
    closing_range = Column(String(8))
    settlement_price = Column(String(8))
    point_change = Column(String(8))
    delta = Column(String(8))
    exercises = Column(String(8))
    volume_trades_cleared = Column(String(8))
    open_interest = Column(String(8))
    open_interest_delta = Column(String(8))
    contract_high = Column(String(8))
    contract_low = Column(String(8))


class DailyBulletinReportsDataType(Base):
    __tablename__ = 'dailybulletin_reports_data_type'
    # Column
    report_id = Column(Integer, ForeignKey('dailybulletin_reports_data.id'), primary_key=True)
    section = Column(String(8), ForeignKey('dailybulletin_sections.section'), primary_key=True)
    contract = Column(String(5), ForeignKey('dailybulletin_contracts.contract'), primary_key=True)
    product = Column(String(4), ForeignKey('dailybulletin_products.globex'), primary_key=True)
    strike = Column(String(8), primary_key=True)
    type = Column(String(8))


class DailyBulletinProducts(Base):
    __tablename__ = 'dailybulletin_products'
    # Column
    id = Column(SmallInteger, primary_key=True)
    name = Column(String(64))
    type = Column(String(16))
    globex = Column(String(4), ForeignKey('unique_globex.globex'), index=True)
    clearing = Column(String(4))
    # Relationship
    unique_globex = relationship("UniqueGlobex", backref="dailybulletin_products")


class DailyBulletinReportsStatus(Base):
    __tablename__ = 'dailybulletin_reports_status'
    # Column
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


class DailyBulletinProductsSymbol(Base):
    __tablename__ = 'dailybulletin_products_symbol'
    # Column
    product_id = Column(SmallInteger, primary_key=True)
    symbol_globex = Column(String(5), primary_key=True)


class DailyBulletinContractsSymbolMonth(Base):
    __tablename__ = 'dailybulletin_contracts_symbol_month'
    # Column
    month_literal = Column(String(1), primary_key=True)
    month_number = Column(SmallInteger)


class DictionaryYear(Base):
    __tablename__ = 'dictionary_year'
    # Column
    year = Column(String(4), primary_key=True)
