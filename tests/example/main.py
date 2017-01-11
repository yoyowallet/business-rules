import datetime
import logging

from business_rules import run_all
from tests.example.actions import ExampleActions
from tests.example.basket import Item, Basket
from tests.example.validators import ExampleValidators
from tests.example.variables import ExampleVariables

logging.basicConfig(level=logging.DEBUG)

rules = [
    {
        "conditions": {
            "all": [
                {
                    "name": "items",
                    "operator": "contains",
                    "value": 1,
                },
                {
                    "name": "current_month",
                    "operator": "equal_to",
                    "value": "January",
                },
                {
                    "name": "current_month_boolean",
                    "operator": "is_true",
                    "value": "True",
                    "params": {
                        "month": datetime.datetime.now().strftime("%B")
                    }
                },
                {
                    "name": "current_year_boolean",
                    "operator": "is_true",
                    "value": "True",
                    "params": {
                        'year': datetime.datetime.now().year
                    }
                },
                {
                    "name": "rule_variable",
                    "operator": "is_true",
                    "value": "True"
                }
            ]
        },
        "actions": [
            {
                "name": "award_stamps",
                "params": {
                    "stamps": 1,
                },
            },
        ],
    },
]

hot_drink = Item(code=1, name='Hot Drink', line_number=1, quantity=1)
basket = Basket(id=0, items=[hot_drink])
run_all(
    rule_list=rules,
    defined_variables=ExampleVariables(basket),
    defined_actions=ExampleActions(basket),
    defined_validators=ExampleValidators(basket),
)