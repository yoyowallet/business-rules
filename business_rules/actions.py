import inspect
from dataclasses import dataclass
from typing import Optional

from .utils import fn_name_to_pretty_label, get_valid_fields


class BaseActions(object):
    """Classes that hold a collection of actions to use with the rules
    engine should inherit from this.
    """

    @classmethod
    def get_all_actions(cls):
        methods = inspect.getmembers(cls)
        return [
            {'name': m[0], 'label': m[1].label, 'params': m[1].params}
            for m in methods
            if getattr(m[1], 'is_rule_action', False)
        ]


def _validate_action_parameters(func, params):
    """
    Verifies that the parameters specified are actual parameters for the
    function `func`, and that the field types are FIELD_* types in fields.
    :param func:
    :param params:
                {
                 'label': 'action_label',
                 'name': 'action_parameter',
                 'fieldType': 'numeric',
                 'defaultValue': 123
                }
    :return:
    """
    if params is not None:
        # Verify field name is valid
        valid_fields = get_valid_fields()

        for param in params:
            param_name, field_type = param['name'], param['fieldType']
            if param_name not in func.__code__.co_varnames:
                raise AssertionError(
                    "Unknown parameter name {0} specified for action {1}".format(
                        param_name, func.__name__
                    )
                )

            if field_type not in valid_fields:
                raise AssertionError(
                    "Unknown field type {0} specified for action {1} param {2}".format(
                        field_type, func.__name__, param_name
                    )
                )


def rule_action(label=None, params=None):
    """
    Decorator to make a function into a rule action.
    `params` parameter could be one of the following:
    1. Dictionary with params names as keys and types as values
    Example:
    params={
        'param_name': fields.FIELD_NUMERIC,
    }

    2. If a param has a default value, ActionParam can be used. Example:
    params={
        'action_parameter': ActionParam(field_type=fields.FIELD_NUMERIC, default_value=123)
    }

    :param label: Label for Action
    :param params: Parameters expected by the Action function
    :return: Decorator function wrapper
    """

    def wrapper(func):
        params_ = params
        if isinstance(params, dict):
            params_ = [
                dict(
                    label=fn_name_to_pretty_label(key),
                    name=key,
                    fieldType=getattr(value, "field_type", value),
                    defaultValue=getattr(value, "default_value", None),
                )
                for key, value in params.items()
            ]

        _validate_action_parameters(func, params_)

        func.is_rule_action = True
        func.label = label or fn_name_to_pretty_label(func.__name__)
        func.params = params_

        return func

    return wrapper


@dataclass
class ActionParam:
    field_type: type
    default_value: Optional[int]
