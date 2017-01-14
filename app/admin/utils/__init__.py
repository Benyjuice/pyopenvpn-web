from openvpn_status import parse_status
from flask import current_app


class utils:
    def __init__(self):
        self.logfile = open(current_app.config['OPENVPN_LOGFILE'])
        if not self.logfile:
            current_app.logger.warning("OpenVPN logfile error: %s open faild." % current_app.config['OPENVPN_LOGFILE'])
        else:
            current_app.logger.info('Openvpn logfile open success')

    def get_user(self):
        status = parse_status(self.logfile.read())
        return status.client_list
