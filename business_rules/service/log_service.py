import logging


class LogService(object):
    def __init__(self):
        super(LogService, self).__init__()
        self.logger = logging.getLogger(__name__)

    def log_rule(self, rule, conditions_met, actions_triggered):
        self.logger.info('rule={} - conditions = {} - actions = {}'.format(rule, conditions_met, actions_triggered))
