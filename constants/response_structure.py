from fastapi import status


class ResponseStructure:
    def __init__(self, response):
        self.response = response
        self.status_code_map = {
            "400": status.HTTP_400_BAD_REQUEST,
            "401": status.HTTP_401_UNAUTHORIZED,
            "404": status.HTTP_404_NOT_FOUND,
            "500": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "200": status.HTTP_200_OK
        }

    def common_success(self, message, api_status_code: str = "200", data=None):
        self.response.status_code = self.status_code_map.get(api_status_code)
        response = {"status": "success", "message": message}
        if data:
            response["data"] = data
        return response

    def common_failure(self, message, api_status_code: str = "400", error=None):
        self.response.status_code = self.status_code_map.get(api_status_code)
        response = {"status": "failed", "message": message}
        if error:
            response["error"] = error
        return response

    def database_error(self):
        return self.common_failure(message="Failed to do the Database transaction.", api_status_code="500")

    def internal_error(self, error="Something went wrong"):
        return self.common_failure(message="Internal error",
                              api_status_code="500",
                              error=str(error))