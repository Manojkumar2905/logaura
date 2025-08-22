from functools import wraps
from http.client import responses
from fastapi import Response, HTTPException
from constants.response_structure import ResponseStructure


def set_response(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        response: Response = kwargs.get('response')
        if not response:
            raise HTTPException(status_code=500, detail="Response is not provided.")
        kwargs['api_response'] = ResponseStructure(response=response)
        return await func(*args, **kwargs)

    return wrapper
