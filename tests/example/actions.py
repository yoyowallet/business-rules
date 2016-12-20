import logging

from business_rules.actions import *
from business_rules.fields import *

logger = logging.getLogger(__name__)


class ExampleActions(BaseActions):
    def __init__(self, basket):
        self.basket = basket

    @rule_action(params={
        "stamps": FIELD_NUMERIC
    }, inject_rule=True)
    def award_stamps(self, stamps, rule):
        logger.info('Awarding {} stamps to basket id: {}'.format(
            stamps,
            self.basket.id,
        ))
        logger.info('rule from ACTION: {}'.format(rule))
        pass
