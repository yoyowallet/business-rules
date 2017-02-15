import inspect
from decimal import Decimal, Inexact, Context

import fields, engine
from util import method_type


def fn_name_to_pretty_label(name):
    return ' '.join([w.title() for w in name.split('_')])


def export_rule_data(variables, actions):
    """
    Export_rule_data is used to export all information about the
    variables, actions, and operators to the client. This will return a
    dictionary with three keys:
    - variables: a list of all available variables along with their label, type, options and params
    - actions: a list of all actions along with their label and params
    - variable_type_operators: a dictionary of all field_types -> list of available operators
    :param variables:
    :param actions:
    :return:
    """
    from . import operators
    actions_data = actions.get_all_actions()
    variables_data = variables.get_all_variables()
    variable_type_operators = {}
    for variable_class in inspect.getmembers(operators, lambda x: getattr(x, 'export_in_rule_data', False)):
        variable_type = variable_class[1]  # getmembers returns (name, value)
        variable_type_operators[variable_type.name] = variable_type.get_all_operators()

    return {"variables": variables_data,
            "actions": actions_data,
            "variable_type_operators": variable_type_operators}


def float_to_decimal(f):
    """
    Convert a floating point number to a Decimal with
    no loss of information. Intended for Python 2.6 where
    casting float to Decimal does not work.
    """
    n, d = f.as_integer_ratio()
    numerator, denominator = Decimal(n), Decimal(d)
    ctx = Context(prec=60)
    result = ctx.divide(numerator, denominator)
    while ctx.flags[Inexact]:
        ctx.flags[Inexact] = False
        ctx.prec *= 2
        result = ctx.divide(numerator, denominator)
    return result


def get_valid_fields():
    valid_fields = [getattr(fields, f) for f in dir(fields) if f.startswith("FIELD_")]
    return valid_fields


def params_dict_to_list(params):
    """
    Transform parameters in dict format to list of dictionaries with a standard format.
    If 'params' is not a dictionary, then the result will be 'params'
    :param params: Dictionary of parameters with the following format:
    {
        'param_name': param_type
    }
    :return:
    [
        {
            'label': 'param_name'
            'name': 'param_name'
            'field_type': param_type
        }
    ]
    """
    if params is None:
        return []

    if not isinstance(params, dict):
        return params

    return [
        {
            'label': fn_name_to_pretty_label(name),
            'name': name,
            'field_type': param_field_type
        } for name, param_field_type in params.items()
    ]


def validate_rule_data(variables, actions, rule):
    """
    validate_rule_data is used to check a generated rule against a set of variables and actions
    :param variables:
    :param actions:
    :param rule:
    :return: bool
    """
    def validate_root_keys(rule):
        root_keys = rule.keys()
        if 'actions' not in root_keys:
            raise AssertionError('Missing "{}" key'.format('actions'))
        if 'conditions' not in root_keys:
            raise AssertionError('Missing "{}" key'.format('conditions'))

    def validate_condition_operator(condition, rule_schema):
        for item in rule_schema.get('variables'):
            if item.get('name') == condition.get('name'):
                condition_field_type = item.get('field_type')
                variable_operators = rule_schema.get('variable_type_operators', {}).get(condition_field_type, [])
                for operators in variable_operators:
                    if operators['name'] == condition['operator']:
                        return True
                raise AssertionError('Unknown operator "{}"'.format(condition['operator']))

    def validate_conditions(input_conditions, rule_schema):
        if isinstance(input_conditions, list):
            for condition in input_conditions:
                validate_conditions(condition, rule_schema)
        if isinstance(input_conditions, dict):
            keys = input_conditions.keys()
            if 'any' in keys or 'all' in keys:
                if len(keys) > 1:
                    raise AssertionError('Expected ONE of "any" or "all" but found {}'.format(keys))
                else:
                    for k, v in input_conditions.iteritems():
                        validate_conditions(v, rule_schema)
            else:
                validate_condition_operator(input_conditions, rule_schema)
                condition_name = input_conditions.get('name')
                if not condition_name:
                    raise AssertionError('Missing condition "name" key in {}'.format(input_conditions))
                if not hasattr(variables, condition_name):
                    raise AssertionError('Unknown condition "{}"'.format(condition_name))
                method = getattr(variables, input_conditions.get('name'))
                params = input_conditions.get('params', {})
                engine._check_params_valid_for_method(method, params, method_type.METHOD_TYPE_VARIABLE)

    def validate_actions(input_actions):
        for action in input_actions:
            method = getattr(actions, action.get('name'))
            params = action.get('params', {})
            engine._check_params_valid_for_method(method, params, method_type.METHOD_TYPE_ACTION)

    rule_schema = export_rule_data(variables, actions)
    validate_root_keys(rule)
    validate_conditions(rule.get('conditions'), rule_schema)
    validate_actions(rule.get('actions'))
    return True
