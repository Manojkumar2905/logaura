from . import get_curl
from constants.common_imports import *
from loggers.log_func import *
from loggers.middleware_loogers import logger


def set_log_details(func):
    @wraps(func)
    async def decorator(request: Request, *args, **kwargs):
        curl_req = ''
        try:
            curl_req = await get_curl(request[2])
        except Exception:
            pass

        required_obj = {k: v for k, v in kwargs.items() if k not in ['api_response', 'response', 'log_vals']}
        log_vals = {k: v for k, v in kwargs.items() if k in 'log_vals'}
        log_vals = log_vals['log_vals']

        data = []
        try:
            for k, models in required_obj.items():
                try:
                    data.append(models.dict())
                except Exception as e:
                    pass
        except Exception as e:
            print(str(e))

        if isinstance(request, list):
            logger.info(msg='Request Log',
                        extra=get_extra_values(userid=request[0], api_id=log_vals, data=data, curl_req=curl_req))
            request.pop()
        else:
            useable_vals = ''
            for vals in data:
                if 'mobile' in vals:
                    useable_vals = vals['mobile']
            logger.info(msg='Request Log', extra=get_extra_values(userid=useable_vals, api_id=log_vals, data=data,
                                                                  curl_req=curl_req))

        return await func(request,
                          *args,
                          **kwargs)

    return decorator
