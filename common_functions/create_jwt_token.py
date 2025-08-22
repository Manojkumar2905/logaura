from . import *
from datetime import datetime, timedelta


def create_access_token(req_info: dict, expiry_time_min: int = None):
    req_info['exp'] = datetime.utcnow() + timedelta(
        minutes=expiry_time_min if expiry_time_min else int(settings.JWT_EXPIRY_TIME_MIN))
    return jwt.encode(req_info, settings.JWT_SECRET_KEY, algorithm="HS256")
