from . import *
from .email_functions import *


class EmailGoogleAuth(BaseModel):
    email: str
    google_client_id: str


error_msg = {
    "otp_expired": "The entered OTP is expired.",
    "invalid_otp": "The entered OTP is Invalid.",
    "email_not_exists": "The email entered does not exists."
}


@app.post(f"{NRI_BASE_ENDPOINT}verify/email/google_auth/", tags=["verification"])
@jwt_token_required
async def verify_email_by_google(request: Request, api_response: Response, obj: EmailGoogleAuth):
    client_id = ObjectId(request[0])
    try:
        if not is_validate_email(obj.email.lower()):
            return common_failure(message="Invalid Email ID.", api_response=api_response)
        if obj.google_client_id != settings.GOOGLE_CLIENT_ID:
            return common_failure(message="Google client id is not correct.", api_response=api_response,
                                  api_status_code="400")
        return email_verification(api_response=api_response, client_id=client_id, verification_from='google',
                                  email=obj.email.lower())
    except Exception as e:
        return internal_error(api_response=api_response)
