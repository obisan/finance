import pandas as pd

from helpers.settings import cl_setting_helper


class cl_utils:

    @staticmethod
    def get_data_by_commodities(path, commodities, user_report_axis):
        axis_x = cl_setting_helper.get_axis_x(user_report_axis)
        axis_y = cl_setting_helper.get_axis_y(user_report_axis)
        axis_z = cl_setting_helper.get_axis_z(user_report_axis)
        axis_all = [axis_x] + axis_y

        result = []

        df = pd.read_csv(path)
        for commodity in commodities:
            df2 = pd.DataFrame(
                df.loc[df[axis_z] == commodity['name_commodity']],
                columns=axis_all)

            df2.sort_values(by=[axis_x], inplace=True, ascending=True)

            l_commodity = commodity['name_commodity'].replace('/', '-')

            s = l_commodity, df2
            result.append(s)

        return result

    @staticmethod
    def get_data(path):
        df = pd.read_csv(path)
        return df