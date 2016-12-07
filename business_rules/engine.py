import logging
from .fields import FIELD_NO_INPUT

logger = logging.getLogger(__name__)

def run_all(rule_list,
            defined_variables,
            defined_actions,
            defined_validators=None,
            stop_on_first_trigger=False):

    rule_was_triggered = False
    for rule in rule_list:
        result = run(rule, defined_variables, defined_actions, defined_validators)
        if result:
            rule_was_triggered = True
            if stop_on_first_trigger:
                return True
    return rule_was_triggered

def run(rule, defined_variables, defined_actions, defined_validators):
    conditions, actions = rule['conditions'], rule['actions']
    rule_triggered, payload = check_conditions_recursively(conditions, defined_variables, [])
    if rule_triggered:
        do_actions(actions, defined_actions, defined_validators, payload)
        return True
    return False

def check_conditions_recursively(conditions, defined_variables, matches):
    keys = list(conditions.keys())
    if keys == ['all']:
        assert len(conditions['all']) >= 1
        for condition in conditions['all']:
            if not check_conditions_recursively(condition, defined_variables, matches):
                return False
        return True, matches

    elif keys == ['any']:
        assert len(conditions['any']) >= 1
        for condition in conditions['any']:
            if check_conditions_recursively(condition, defined_variables, matches):
                return True, matches
        return False

    else:
        # help prevent errors - any and all can only be in the condition dict
        # if they're the only item
        assert not ('any' in keys or 'all' in keys)
        result = check_condition(conditions, defined_variables)
        matches.append(result)
        return result[0], matches

def check_condition(condition, defined_variables):
    """ Checks a single rule condition - the condition will be made up of
    variables, values, and the comparison operator. The defined_variables
    object must have a variable defined for any variables in this condition.
    """
    name, op, value = condition['name'], condition['operator'], condition['value']
    operator_type = _get_variable_value(defined_variables, name)
    return _do_operator_comparison(operator_type, op, value), name, op, value

def _get_variable_value(defined_variables, name):
    """ Call the function provided on the defined_variables object with the
    given name (raise exception if that doesn't exist) and casts it to the
    specified type.

    Returns an instance of operators.BaseType
    """
    def fallback(*args, **kwargs):
        raise AssertionError("Variable {0} is not defined in class {1}".format(
                name, defined_variables.__class__.__name__))
    method = getattr(defined_variables, name, fallback)
    val = method()
    return method.field_type(val)

def _do_operator_comparison(operator_type, operator_name, comparison_value):
    """ Finds the method on the given operator_type and compares it to the
    given comparison_value.

    operator_type should be an instance of operators.BaseType
    comparison_value is whatever python type to compare to
    returns a bool
    """
    def fallback(*args, **kwargs):
        raise AssertionError("Operator {0} does not exist for type {1}".format(
            operator_name, operator_type.__class__.__name__))
    method = getattr(operator_type, operator_name, fallback)
    if getattr(method, 'input_type', '') == FIELD_NO_INPUT:
        return method()
    return method(comparison_value)

def do_actions(actions, defined_actions, defined_validators, payload):

    def action_fallback(*args, **kwargs):
        raise AssertionError("Action {0} is not defined in class {1}"\
            .format(method_name, defined_actions.__class__.__name__))

    def validator_fallback(*args, **kwargs):
        # return True by default if no validation function provided
        # might need to override this with some default behaviour?
        return True

    for action in actions:
        method_name = action['name']
        params = action.get('params') or {}

        valid = [
            getattr(
                defined_validators,
                condition_result[1],
                validator_fallback,
            )(condition_result[2], condition_result[3])
            for condition_result in payload
        ]
        if not any(valid):
            logger.info('Already awarded loyalty for action: {action}'.format(action=method_name))

        method = getattr(defined_actions, method_name, action_fallback)
        method(**params)
