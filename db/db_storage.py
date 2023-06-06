import configparser

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class CotReportType(Base):
    __tablename__ = 'cot_report_type'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Setting(Base):
    __tablename__ = 'setting'

    id = Column(Integer, primary_key=True)
    param_name = Column(String)
    param_value = Column(String)


class DailyBulletinReports(Base):
    __tablename__ = 'dailybulletin_reports'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    date = Column(String)
    index = Column(Integer)
    path = Column(String(255))
    status = Column(String(16))


class DailyBulletinReportsStatus(Base):
    __tablename__ = 'dailybulletin_reports'

    status = Column(String(16), primary_key=True)


class DailyBulletinSections(Base):
    __tablename__ = 'dailybulletin_sections'

    section = Column(String(8), primary_key=True)
    type = Column(String(8))


class DailyBulletinSectionsNames(Base):
    __tablename__ = 'dailybulletin_sections_names'

    section = Column(String(8), primary_key=True)
    name = Column(String(255))


class DailyBulletinSectionsSubsections(Base):
    __tablename__ = 'dailybulletin_sections_subsections'

    section = Column(String(8), primary_key=True)
    seq = Column(Integer, primary_key=True)
    name = Column(String(255))


class DailyBulletinSectionsTypes(Base):
    __tablename__ = 'dailybulletin_sections_types'

    type = Column(String(8), primary_key=True)


class StorageDb:

    def __init__(self, host=None, port=None, dbname=None, user=None, password=None, filename=None):
        if filename:
            self._init_from_file(filename)
        else:
            self._init_from_params(host, port, dbname, user, password)

    def _init_from_file(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)

        host = config['DEFAULT']['host']
        port = config['DEFAULT']['port']
        dbname = config['DEFAULT']['dbname']
        user = config['DEFAULT']['user']
        password = config['DEFAULT']['password']

        self._init_from_params(host, port, dbname, user, password)

    def _init_from_params(self, host, port, dbname, user, password):
        connection_string = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
        self.engine = create_engine(connection_string)
        self.session = sessionmaker(bind=self.engine)

    def get_cot_report_type(self):
        return self.session().query(CotReportType).all()

    def get_setting(self, param_name):
        return self.session().query(
            func.replace(Setting.param_value, ' ', '')).filter_by(param_name=param_name).scalar()

    def get_dailybulletin_reports(self):
        return self.session().query(
            func.replace(DailyBulletinReports.name, ' ', ''),
            func.replace(DailyBulletinReports.path, ' ', '')).all()

    def get_dailybulletin_reports_by_names(self, names):
        return self.session().query(
            DailyBulletinReports.id,
            func.replace(DailyBulletinReports.name, ' ', '')). \
            filter(DailyBulletinReports.name.in_(names)).all()

    def get_dailybulletin_sections_by_section(self, sections):
        return self.session().query(
            DailyBulletinSectionsSubsections.section,
            func.replace(DailyBulletinSections.name, ' ', '')). \
            filter(DailyBulletinSectionsSubsections.section.in_(sections)).all()

    def insert_dailybulletin_reports(self, name, date, index, path, status):
        report = DailyBulletinReports(name=name, date=date, index=index, path=path, status=status)
        self.session().add(report)
        self.session().commit()
