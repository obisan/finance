class cl_setting_helper:

    @staticmethod
    def get_zip_path(r_settings, year):
        return r_settings['system']['path'] + \
               r_settings['service']['param1'] + \
               str(year) + '.' + \
               r_settings['system']['extension2']

    @staticmethod
    def get_axis(report_axis):
        x_axis = \
            list(filter(lambda x: (x['axis'] == 'X') & (x['hide'] == '-'), report_axis))[0]['name']

        y_axis = \
            [x['name'] for x in list(filter(lambda x: (x['axis'] == 'Y') & (x['hide'] == '-'), report_axis))]

        hide = \
            [x['name'] for x in list(filter(lambda x: (x['hide'] == 'X'), report_axis))]

        key = \
            list(filter(lambda x: x['key'] == 'X', report_axis))[0]['name']

        return x_axis, y_axis, hide, key

    @staticmethod
    def get_axis_x(user_report_axis):
        x_axis = \
            list(filter(lambda x: (x['axis'] == 'X') & (x['hide'] == '-'), user_report_axis))[0]['name']
        return x_axis

    @staticmethod
    def get_axis_y(user_report_axis):
        y_axis = \
            [x['name'] for x in list(filter(lambda x: (x['axis'] == 'Y') & (x['hide'] == '-'), user_report_axis))]
        return y_axis

    @staticmethod
    def get_axis_z(user_report_axis):
        z_axis = \
            list(filter(lambda x: (x['axis'] == 'Z'), user_report_axis))[0]['name']
        return z_axis

    @staticmethod
    def get_axis_key(user_report_axis):
        key = \
            list(filter(lambda x: x['key'] == 'X', user_report_axis))[0]['name']
        return key

    @staticmethod
    def get_axis_hide(user_report_axis):
        hide = \
            [x['name'] for x in list(filter(lambda x: (x['hide'] == 'X'), user_report_axis))]
        return hide

    @staticmethod
    def get_axis_all(axis):
        return [axis[0]] + axis[1]

    @staticmethod
    def get_axis_commodity(axis):
        return axis[3]
