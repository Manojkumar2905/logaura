from constants.common_imports import status

status_code_map = {
    "400": status.HTTP_400_BAD_REQUEST,
    "401": status.HTTP_401_UNAUTHORIZED,
    "404": status.HTTP_404_NOT_FOUND,
    "500": status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def common_failure(message, api_status_code: str = "400", api_response=None, error=None):
    api_response.status_code = status_code_map.get(api_status_code)
    response = {"status": "failed", "message": message}
    if error:
        response["error"] = error
    return response


def database_error(api_response):
    return common_failure(message="Failed to do the Database transaction.", api_response=api_response,
                          api_status_code="500")


def internal_error(api_response, error="Something went wrong."):
    return common_failure(message="Internal error.",
                          api_response=api_response,
                          api_status_code="500",
                          error=str(error))

