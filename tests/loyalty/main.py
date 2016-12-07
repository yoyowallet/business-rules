import logging
from business_rules import run_all
from tests.loyalty.basket import Item, Basket
from tests.loyalty.variables import LoyaltyVariables
from tests.loyalty.actions import LoyaltyActions
from tests.loyalty.validators import LoyaltyValidators

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
                    "value": "December",
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
    defined_variables=LoyaltyVariables(basket),
    defined_actions=LoyaltyActions(basket),
    defined_validators=LoyaltyValidators(basket),
)
