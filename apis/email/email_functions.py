from common_functions.create_jwt_token import create_access_token
from . import *
from nri.V1.stage_functions import *

error_msg = {
    "otp_expired": "The entered OTP is expired.",
    "invalid_otp": "The entered OTP is Invalid.",
    "wrong_email": "Wrong email."
}
def get_next_application_number():
    last_entry = COL_NRI.find_one({}, sort=[("application_no", -1)])
    if last_entry and 'application_no' in last_entry:
        last_number = last_entry['application_no']
        numeric_part = int(last_number[2:]) if last_number != '' else 0
        next_number = numeric_part + 1
        return f"{settings.APPLICATION_SERIES}{next_number:08d}"
    else:
        return f"{settings.APPLICATION_SERIES}00000001"

def email_verification(api_response, client_id, verification_from, email: str, otp=None):
    email = email.lower()

    customer_details = COL_NRI.find_one({"_id": client_id},
                                         {"stages": 1, "email": 1, "_id": 0})
    if not customer_details:
        return common_failure(message="No client found.", api_response=api_response)
    if verification_from == 'manual':
        if customer_details['email']['id'] != email:
            return common_failure(message=error_msg["wrong_email"], api_response=api_response)

        if not customer_details['email']['otp'] == otp:
            return common_failure(message=error_msg["invalid_otp"], api_response=api_response)

        if not is_validation_time_within_30_minutes(customer_details['email']['otp_ts']):
            return common_failure(message=error_msg["otp_expired"], api_response=api_response)

        email_val_update = {
            "$set": {
                "current_stage": get_next_stage(
                    COL_NRI.find_one({"_id": client_id}, {"stages": 1, "_id": 0})['stages']),
                # "email.id": email,
                # "email.otp": otp,
                # "email.otp_ts": convert_datetime_ist(datetime.now()),
                "email.is_verified": True,
                "email.is_google_verified": False,
                "nri_logs.email_verified_ts": convert_datetime_ist(datetime.now()),
                "application_no": get_next_application_number(),
                "event_ts.created_ts": convert_datetime_ist(datetime.now()),
                "nri_logs.mobile_verified_ts": convert_datetime_ist(datetime.now()),
                "bool_vals.is_deleted": False
            }
        }
        COL_NRI.update_one({"_id": client_id}, email_val_update)
    else:
        email_val_update = {
            "$set": {
                "current_stage": get_next_stage(
                    COL_NRI.find_one({"_id": client_id}, {"stages": 1, "_id": 0})['stages']),
                # "email.id": email,
                "email.is_verified": True,
                "email.is_google_verified": True,
                "nri_logs.email_verified_ts": convert_datetime_ist(datetime.now()),
                "application_no": get_next_application_number(),
                "event_ts.created_ts": convert_datetime_ist(datetime.now()),
                "nri_logs.mobile_verified_ts": convert_datetime_ist(datetime.now()),
                "bool_vals.is_deleted": False
            }
        }
        COL_NRI.update_one({"_id": client_id}, email_val_update)

    stage_name = get_next_stage(customer_details['stages'])
    access_token = create_access_token({'client_id': ObjectId(client_id)})
    return common_success(message="Email verification success.", api_response=api_response,
                          data={
                              "next_stage": stage_name,
                              "access_token": access_token,
                              "completed_stages": get_complete_stages(customer_details['stages'])
                          })
