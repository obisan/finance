from helpers.loader import Loader
from helpers.plotter import Plotter


class futures:

    def __init__(self, user_report, user_report_commodity, user_report_axis, settings, target_year):
        self.user_report = user_report
        self.user_report_commodity = user_report_commodity
        self.user_report_axis = user_report_axis
        self.settings = settings
        self.target_year = target_year

    def run(self):

        loader = \
            Loader(
                self.user_report,
                self.user_report_commodity,
                self.user_report_axis,
                self.settings,
                self.target_year)

        if loader.run() != 0:
            return 1

        data = loader.get_data()

        # loader.save2db()

        # return 0

        plotter = Plotter(self.user_report_axis, self.settings, self.target_year)

        if plotter.draw(data) != 0:
            return 2

        return 0
