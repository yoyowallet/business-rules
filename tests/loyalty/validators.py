import logging

logger = logging.getLogger(__name__)


class LoyaltyValidators(object):
    def __init__(self, basket):
        self.basket = basket

    def items(self, operator, value):
        logger.debug('operator={}, value={}'.format(operator, value))
        # TODO validation logic
        return True

    def current_month(self, operator, value):
        logger.debug('operator={}, value={}'.format(operator, value))
        # TODO validation logic
        return True
