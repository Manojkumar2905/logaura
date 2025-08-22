from constants.common_imports import *

status_code_map = {
    "200": status.HTTP_200_OK
}


def common_success(message, api_status_code: str = "200", api_response=None, data=None):
    api_response.status_code = status_code_map.get(api_status_code)
    response = {"status": "success", "message": message}
    if data:
        response["data"] = data
    return response


def stage_details_success(current_stage, next_stage, completed_stages, data=None, api_status_code: str = "200",
                          api_response=None):
    api_response.status_code = status_code_map.get(api_status_code)
    # TODO if any additional data is there add it inside the "data" key
    return {
        "status": "success",
        # "data": data if data else {},
        "message": "Successfully fetched stage details.",
        "data": {
            "current_stage": current_stage,
            "next_stage": next_stage,
            "completed_stages": completed_stages if completed_stages else []
        }

    }
