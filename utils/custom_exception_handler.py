from rest_framework.views import exception_handler
from django.http import JsonResponse
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR ,HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

# sets status=True for 2xx codes 
def get_response(message="", result={}, status=False, status_code=HTTP_400_BAD_REQUEST):
    if str(status_code)[0] == "2":
        status=True    
    return {
        "message" : message,
        "result" : result,
        "status" : status,
        "status_code" : status_code,
    }
 
def get_error_message(error_dict):
   field = next(iter(error_dict))
   response = error_dict[next(iter(error_dict))]
   if isinstance(response, dict):
       response = get_error_message(response)
   elif isinstance(response, list):
       response_message = response[0]
       if isinstance(response_message, dict):
           response = get_error_message(response_message)
       else:
           response = response[0]
   return response
 
def handle_exception(exc, context):
   error_response = exception_handler(exc, context)
   if error_response is not None:
       error = error_response.data
 
       if isinstance(error, list) and error:
           if isinstance(error[0], dict):
               error_response.data = get_response(
                   message=get_error_message(error),
                   status_code=error_response.status_code,
               )
 
           elif isinstance(error[0], str):
               error_response.data = get_response(
                   message=error[0],
                   status_code=error_response.status_code
               )
 
       if isinstance(error, dict):
           error_response.data = get_response(
               message=get_error_message(error),
               status_code=error_response.status_code
           )
   return error_response
 
class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
    
        response = self.get_response(request)
        status_in = response.status_code

        if response.status_code == 500:
            return JsonResponse(get_response(message="Internal server error, please try again later",
                                            status_code=HTTP_500_INTERNAL_SERVER_ERROR),
                                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        if response.status_code == 404 and "Page not found" in str(response.content):
            return JsonResponse(get_response(message="Page not found, invalid url",
                                            status_code=HTTP_404_NOT_FOUND),
                                            status=HTTP_404_NOT_FOUND)

    # CHANGING 2XX to known 2XX codes
        if status_in == 261:
            return JsonResponse(get_response(message="Late entry registered", 
                                            status_code=HTTP_201_CREATED),
                                            status=HTTP_201_CREATED)

        if status_in == 260:
            return JsonResponse(get_response(message="Successfully logged in",
                                            status_code=HTTP_200_OK),
                                            status=HTTP_200_OK)

    # CHANGING ALL 4XX to 400 Bad request (DEFAULT)
        if status_in == 460:
            return JsonResponse(get_response(message="Student data doesn\'t exist or incorrect venue entered"),status=HTTP_400_BAD_REQUEST)

        if status_in == 461:
            return JsonResponse(get_response(message="Venue not entered"),status=HTTP_400_BAD_REQUEST)

        if status_in == 462:
            return JsonResponse(get_response(message="Late entry already registered"),status=HTTP_400_BAD_REQUEST)

    # CHANGING ALL 4XX to 403 Forbidden
        if status_in == 463:
            return JsonResponse(get_response(message="Incorrect password",
                                            status_code=HTTP_403_FORBIDDEN),
                                            status=HTTP_403_FORBIDDEN)

        if status_in == 464:
            return JsonResponse(get_response(message="No matching user found",
                                            status_code=HTTP_403_FORBIDDEN),
                                            status=HTTP_403_FORBIDDEN)

        return response