from rest_framework.views import exception_handler
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # If the error is "Method Not Allowed" (405)
    if response is not None and response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        response.data = {
            'status': 'error',
            'message': f"The action you tried ({context['request'].method}) is not allowed on this page."
        }
    
    # You can add more customizations for other status codes here
    # For example, 404 (Not Found)
    elif response is not None and response.status_code == status.HTTP_404_NOT_FOUND:
        response.data = {
            'status': 'error',
            'message': 'The requested resource was not found.'
        }

    return response
