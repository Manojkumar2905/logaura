import json

from . import *


class EmailOTP(BaseModel):
    email: str


err_map = {
    'email_exists': 'Email already exists.'
}


@app.post(f"{NRI_BASE_ENDPOINT}verify/email/getotp/", tags=["verification"])
async def generate_email_otp(request: Request, api_response: Response, obj: EmailOTP):
    try:
        COL_NRI=nri_ClientConnection.get_collection(settings.COLLECTION_NRI)
        COL_ONBOARDING_MASTER=nri_ClientConnection.get_collection(settings.COLLECTION_ONBOARDING_MASTER)
        if not is_validate_email(obj.email.lower()):
            return common_failure(message="Invalid Email ID.", api_response=api_response)
        if back_office_check(field_type='EMAIL', data=obj.email):
            return common_failure(message='Email already exists.', api_response=api_response)

        email_details = COL_NRI.find_one({"email.id": obj.email.lower()}, {"email.id": 1, "_id": 1})
        email_otp = get_random_number()
        if not email_details:
            customer_details_obj = COL_ONBOARDING_MASTER.find_one(
                {'doc_type': 'nri_client_structure'}
            )
            customer_details_obj['email']['id'] = obj.email.lower()
            customer_details_obj['email']['otp'] = email_otp
            customer_details_obj['email']['otp_ts'] = convert_datetime_ist(datetime.now())
            customer_details_obj.pop('_id')
            db_resp = COL_NRI.insert_one(document=customer_details_obj)
        else:
            customer_otp_update = {
                "$set": {
                    "email.otp": email_otp,
                    "email.otp_ts": convert_datetime_ist(datetime.now())
                }

            }
            db_resp = COL_NRI.update_one({"_id": ObjectId(email_details['_id'])}, customer_otp_update)
        if not db_resp or not db_resp.acknowledged:
            return common_failure(message="Failed to update.", api_response=api_response)

        email_status = e_notifiers.send_email(sender_email=obj.email.lower(),
                                              subject="OTP for NRI account opening at Firstock",
                                              email_name=settings.EMAIL_VERIFICATION_NAME,
                                              email_temp=settings.EMAIL_VERIFICATION_TEMPLATE,
                                              var_vals={
                                                  "email_otp": email_otp,
                                                  "email_id":obj.email.lower()
                                              })
        if email_status == 'email_sent_success':
            return common_success(message="OTP sent successfully to your email.", api_response=api_response,
                                  data={
                                      "next_stage": "confirm_email_otp"
                                  })
        else:
            response=json.loads(email_status)
            return common_failure(message=response['data']['error'], api_response=api_response, api_status_code="400")
    except Exception as e:
        return internal_error(api_response=api_response)
