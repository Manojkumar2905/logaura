from csv import excel
from logging import exception

from constants.common_imports import *
from constants.config import settings
from database.mongodb.mongodb_common_functions import verify_token
from common_functions.aes_encryption import aesCipher
import jwt


async def validate_token(request: Request):
    basic_auth_token = None
    if 'Authorization' in request.headers:
        basic_auth_token = request.headers["Authorization"].split(" ")[1]
    if not basic_auth_token:
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        jwt_decoded = jwt.decode(basic_auth_token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
    except Exception as error:
        raise HTTPException(status_code=401, detail='Unauthorized')
    if jwt_decoded.get("encrypted", False):
        jwt_decoded["client_id"] = aesCipher.decrypt(jwt_decoded["client_id"])
    is_valid_client_id = verify_token([jwt_decoded["client_id"]])
    return is_valid_client_id, basic_auth_token, jwt_decoded["client_id"]


def jwt_token_required(func):
    @wraps(func)
    async def decorator(request: Request, *args, **kwargs):
        # try:
        validation_result = await validate_token(request=request)
        if validation_result[0]:
            return await func([validation_result[2],
                               validation_result[1],
                               request],
                              *args,
                              **kwargs)
        else:
            raise HTTPException(status_code=401, detail='Unauthorized')
        # except Exception as e:
        #     raise HTTPException(status_code=401, detail='Unauthorized')

    return decorator


async def verify_jwt_token(api_request: Request):
    try:
        validation_result = await validate_token(request=api_request)
        if validation_result[0][0]:
            return validation_result[2]
        else:
            raise HTTPException(status_code=401, detail='Unauthorized')
    except Exception as e:
        raise HTTPException(status_code=401, detail='Unauthorized')
