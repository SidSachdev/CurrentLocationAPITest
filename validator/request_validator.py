import newrelic.agent
from voluptuous import Schema, Required

from constants import ExtractRequestFields


@newrelic.agent.function_trace()
def validate_extract_create_user_visit_input(request):
    """
    Validator functions that accept a request and make sure
    the input matches the allowed schema
    :param request: request
    :return: schema
    """
    schema = Schema(
        {
            Required(ExtractRequestFields.Input.MERCHANT): {
                Required(ExtractRequestFields.Input.MERCHANT_ID): str,
                Required(ExtractRequestFields.Input.MERCHANT_NAME): str,
            },
            Required(ExtractRequestFields.Input.USER): {
                Required(ExtractRequestFields.Input.USER_ID): str
            },
        }
    )
    return schema(request.json)


@newrelic.agent.function_trace()
def validate_extract_all_user_visit_input(request):
    """
    Validator functions that accept a request and make sure
    the input matches the allowed schema
    :param request: request
    :return: schema
    """
    schema = Schema({Required(ExtractRequestFields.Input.SEARCHSTRING): str,})
    return schema(request.to_dict())
