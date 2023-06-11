import configparser

from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db.model import \
    DailyBulletinReports, DailyBulletinSections, DailyBulletinSectionsNames, DailyBulletinProducts, \
    CotReportType, Setting

Base = declarative_base()


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
        with self.session() as session:
            result = session.query(
                func.replace(Setting.param_value, ' ', '')).filter_by(param_name=param_name).scalar()
        return result

    def get_dailybulletin_reports(self):
        with self.session() as session:
            result = session.query(
                func.replace(DailyBulletinReports.name, ' ', ''),
                func.replace(DailyBulletinReports.path, ' ', '')).all()
        return result

    def get_dailybulletin_reports_by_names(self, names):
        with self.session() as session:
            result = session.query(
                DailyBulletinReports.id,
                func.replace(DailyBulletinReports.name, ' ', '')). \
                filter(DailyBulletinReports.name.in_(names)).all()
        return result

    def get_dailybulletin_sections_by_section(self, sections):
        with self.session() as session:
            result = session.query(
                func.replace(DailyBulletinSections.section, ' ', ''),
                func.replace(DailyBulletinSectionsNames.name, ' ', '')
            ).join(
                DailyBulletinSectionsNames,
                DailyBulletinSections.section == DailyBulletinSectionsNames.section
            ).filter(
                DailyBulletinSections.section.in_(sections)
            ).order_by(
                DailyBulletinSections.section,
                DailyBulletinSectionsNames.seq) \
                .all()
        return result

    def get_dailybulletin_products(self):
        with self.session() as session:
            result = session.query(
                DailyBulletinProducts.product_name
            ).all()
        return result

    def insert_dailybulletin_reports(self, name, date, index, path, status):
        with self.session() as session:
            report = DailyBulletinReports(name=name, date=date, index=index, path=path, status=status)
            session.add(report)
            session.commit()
