from matplotlib import pyplot as plt

from helpers.settings import cl_setting_helper


class Plotter:

    def __init__(self, user_report_axis, settings, target_year):
        self.settings = settings
        self.target_year = target_year
        self.user_report_axis = user_report_axis

        self.path = settings['path'] + settings['scr_file'] + str(target_year) + '.' + settings['extension1']

        self.axis_x = cl_setting_helper.get_axis_x(self.user_report_axis)
        self.axis_y = cl_setting_helper.get_axis_y(self.user_report_axis)
        self.hide = cl_setting_helper.get_axis_hide(self.user_report_axis)

    def draw(self, data):

        for l_data in data:
            plt.close('all')
            ax = plt.gca()

            for idy in self.axis_y:
                if idy in self.hide:
                    continue
                l_data[1].plot(kind='line', x=self.axis_x, y=idy, ax=ax)

            plt.title(l_data[0])
            ax.legend(loc='upper center', bbox_to_anchor=(0.25, -0.15),
                      shadow=True, ncol=1)
            plt.show()

        return 0
