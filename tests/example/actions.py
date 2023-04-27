#! python3
import logging

from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT

logger = logging.getLogger(__name__)


class ExampleActions(BaseActions):
    def __init__(self, basket):
        self.basket = basket

    @rule_action(params={"message": FIELD_TEXT})
    def log(self, message, **kargs):
        logger.info(message)
