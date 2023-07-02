import configparser

from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from constants.enums import DailyBulletinReportsDataColumns
from db.model import \
    DailyBulletinReports, DailyBulletinSections, DailyBulletinSectionsNames, DailyBulletinProducts, \
    DailyBulletinReportsData, UniqueGlobex, UniqueGlobexSymbol, CotReportType, Setting, DailyBulletinContracts, \
    DailyBulletinProductsSymbol, DailyBulletinContractsSymbolMonth

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
                func.trim(Setting.param_value)).filter_by(param_name=param_name).scalar()
        return result

    def get_dailybulletin_reports(self):
        with self.session() as session:
            result = session.query(
                func.trim(DailyBulletinReports.name),
                DailyBulletinReports.id,
                func.trim(DailyBulletinReports.path)).all()
        return result

    def get_dailybulletin_reports_by_names(self, names):
        with self.session() as session:
            result = session.query(
                DailyBulletinReports.id,
                func.trim(DailyBulletinReports.name)). \
                filter(DailyBulletinReports.name.in_(names)).all()
        return result

    def get_dailybulletin_sections_by_section(self, sections):
        with self.session() as session:
            result = session.query(
                func.trim(DailyBulletinSections.section),
                func.trim(DailyBulletinSectionsNames.name),
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

    def get_dailybulletin_products(self, product_names):
        with self.session() as session:
            result = session.query(
                func.trim(DailyBulletinProducts.name),
                func.trim(DailyBulletinProducts.type),
                func.trim(DailyBulletinProducts.globex),
                func.trim(DailyBulletinProducts.clearing),
            ).filter(
                DailyBulletinProducts.name.in_(product_names)
            ).all()
        return result

    def insert_dailybulletin_products(self, products):
        with self.session() as session:
            for product in products:
                record = DailyBulletinProducts(
                    name=product['name'],
                    type=product['type'],
                    globex=product['globex'],
                    clearing=product['clearport'])
                session.add(record)
            session.commit()

    def get_unique_globex(self):
        with self.session() as session:
            result = session.query(
                func.trim(UniqueGlobex.globex)).all()
        return result

    def insert_unique_globex(self, globexes):
        with self.session() as session:
            for globex in globexes:
                record = UniqueGlobex(globex=globex)
                session.add(record)
            session.commit()

    def get_unique_globex_symbol(self):
        with self.session() as session:
            result = session.query(
                func.trim(UniqueGlobexSymbol.globex)).all()
        return result

    def insert_unique_globex_symbol(self, globexes):
        with self.session() as session:
            for globex in globexes:
                record = UniqueGlobexSymbol(
                    globex=globex['globex_symbol'])
                session.add(record)
            session.commit()

    def update_dailybulletin_products(self, products):
        s = 0
        # with self.session() as session:
        #     for product in products:
        #         record = DailyBulletinProducts(
        #             product_name=product['product_name'],
        #             type=product['type'],
        #             globex=product['globex'],
        #             clearing=product['clearport'])
        #         session.update(record)
        #     session.commit()

    def insert_dailybulletin_reports(self, dailybulletin_reports):
        with self.session() as session:
            for bulletin in dailybulletin_reports:
                report = DailyBulletinReports(
                    name=bulletin['name'],
                    date=bulletin['date'],
                    index=bulletin['index'],
                    path=bulletin['path'],
                    status=bulletin['status'])
                session.add(report)
            session.commit()

    def insert_dailybulletin_reports_data(self, dailybulletin_reports_data):
        with self.session() as session:
            for bulletin in dailybulletin_reports_data:
                for section in bulletin['data']:
                    for strike in section['strikes']:
                        record = DailyBulletinReportsData(
                            report_id=bulletin['report_id'],
                            section=bulletin['section'],
                            contract=section['contract'],
                            product=section['product'],
                            type=strike[DailyBulletinReportsDataColumns.TYPE.value],
                            strike=strike[DailyBulletinReportsDataColumns.STRIKE.value],
                            strike_index=strike[DailyBulletinReportsDataColumns.STRIKE_INDEX.value],
                            open_range=strike[DailyBulletinReportsDataColumns.OPEN_RANGE.value],
                            high=strike[DailyBulletinReportsDataColumns.HIGH.value],
                            low=strike[DailyBulletinReportsDataColumns.LOW.value],
                            closing_range=strike[DailyBulletinReportsDataColumns.CLOSING_RANGE.value],
                            settlement_price=strike[DailyBulletinReportsDataColumns.SETT_PRICE.value],
                            point_change=strike[DailyBulletinReportsDataColumns.PT_CHGE.value],
                            delta=strike[DailyBulletinReportsDataColumns.DELTA.value],
                            exercises=strike[DailyBulletinReportsDataColumns.EXERCISES.value],
                            volume_trades_cleared=strike[DailyBulletinReportsDataColumns.VOLUME_TRADES_CLEARED.value],
                            open_interest=strike[DailyBulletinReportsDataColumns.OPEN_INTEREST.value],
                            open_interest_delta=strike[DailyBulletinReportsDataColumns.OPEN_INTEREST_DELTA.value],
                            contract_high=strike[DailyBulletinReportsDataColumns.HIGH.value],
                            contract_low=strike[DailyBulletinReportsDataColumns.LOW.value])
                        session.add(record)
            session.commit()

    def insert_dailybulletin_contracts(self, contracts):
        with self.session() as session:
            for contract in contracts:
                record = DailyBulletinContracts(
                    product=contract['product'],
                    symbol=contract['symbol'],
                    year=contract['year'],
                    month=contract['month'],
                    product_group=contract['product_group'],
                    underlying=contract['underlying'],
                    first_avail=contract['first_avail'],
                    expiration=contract['expiration'],
                    settle=contract['settle'],
                    clearing=contract['clearing'],
                    globex=contract['globex'],
                    prs=contract['prs'],
                    floor=contract['floor'],
                    group=contract['group'],
                    itc=contract['itc'],
                    exchange_contract=contract['exchange_contract'],
                    type=contract['type'])
                session.add(record)
            session.commit()

    def get_dailybulletin_products_symbol(self):
        with self.session() as session:
            result = session.query(
                DailyBulletinProductsSymbol.product_id,
                DailyBulletinProductsSymbol.symbol_globex).all()
        return result

    def insert_dailybulletin_products_symbol(self, symbols):
        with self.session() as session:
            for symbol in symbols:
                record = DailyBulletinProductsSymbol(
                    product_id=symbol['product_id'],
                    symbol_globex=symbol['symbol_globex'])
                session.add(record)
            session.commit()

    def get_dailybulletin_report_contracts_symbol_month(self):
        with self.session() as session:
            result = session.query(
                DailyBulletinContractsSymbolMonth.month_literal,
                DailyBulletinContractsSymbolMonth.month_number).all()
        return result
