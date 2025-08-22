from decorators.set_log_details import set_log_details
from decorators.set_response import set_response
from loggers.enums import LOG_EMAIL_VERIFY_EMAIL
from loggers.log_func import get_extra_values
from . import *
from .email_functions import *


class VerifyEmailOTP(BaseModel):
    email: str
    email_otp: str


@app.post(f"{NRI_BASE_ENDPOINT}verify/email/verify_otp/", tags=["verification"])

async def verify_email_otp(request: Request, response: Response, obj: VerifyEmailOTP):
    try:
        COL_NRI = nri_ClientConnection.get_collection(settings.COLLECTION_NRI)
        if not is_validate_email(obj.email.lower()):
            return common_failure(message="Invalid email number.")
        if len(obj.email_otp) != 6 or not obj.email_otp.isdigit():
            return common_failure(message="Invalid OTP.", api_response=response)
        customer_details = COL_NRI.find_one({"email.id": obj.email.lower()},
                                             {"_id": 1, "stages": 1, "email": 1})
        client_id=customer_details['_id']

        return email_verification(client_id=client_id, verification_from='manual', email=obj.email.lower(),
                                  otp=obj.email_otp, api_response=response)
    except Exception as e:
        return e
