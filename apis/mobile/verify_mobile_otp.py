from ekyc.V1.common_api.location_check import geolocator
from common_functions.create_jwt_token import create_access_token
from constants.common_imports import *
from constants.project_imports import *
from ekyc.V1.stage_functions import *


class VerifyMobileOTP(BaseModel):
    mobile: str
    mobile_otp: str
    ref_source: str
    ref_code: str


error_msg = {
    "otp_expired": "The entered OTP is expired.",
    "invalid_otp": "The entered OTP is Invalid.",
    "mobile_not_exists": "The mobile entered does not exists."
}


def get_next_application_number():
    last_entry = COL_EKYC.find_one({"application_no": {"$regex": f"^{settings.APPLICATION_SERIES}"}},
                                   sort=[("application_no", -1)])
    if last_entry and 'application_no' in last_entry:
        last_number = last_entry['application_no']
        numeric_part = int(last_number[2:]) if last_number != '' else 0
        next_number = numeric_part + 1
        return f"{settings.APPLICATION_SERIES}{next_number:08d}"
    else:
        return f"{settings.APPLICATION_SERIES}00000001"


@app.post(f"{EKYC_BASE_ENDPOINT}verify/mobile/verify_otp/", tags=["verification"])
# @set_log_details
@set_response
async def verify_mobile_otp(request: Request, response: Response, obj: VerifyMobileOTP, api_response=None,
                            log_vals=LOG_MOBILE_VERIFY_OTP):
    try:
        if not is_valid_mobile_number(obj.mobile):
            logger.info(msg="Invalid mobile number",
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_failure(message="Invalid mobile number")

        if len(obj.mobile_otp) != 6 or not obj.mobile_otp.isdigit():
            logger.info(msg="Invalid OTP",
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_failure(message="Invalid OTP")

        if len(obj.ref_source) > 50 or len(obj.ref_code) > 50:
            logger.info(msg="Length of referral source or referral code should be less than 50",
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_failure(
                message="Length of referral source or referral code should be less than 50")

        if obj.ref_source == "" or obj.ref_code == "":
            obj.ref_source = "W"
            obj.ref_code = "WEB"

        customer_details = COL_EKYC.find_one({"mobile.number": obj.mobile},
                                             {"mobile": 1, "_id": 1, "stages": 1, "email": 1, "bool_vals": 1})
        if not customer_details:
            logger.info(msg=error_msg["mobile_not_exists"],
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_failure(message=error_msg["mobile_not_exists"])

        if not customer_details['mobile']['otp'] == obj.mobile_otp:
            logger.info(msg=error_msg["invalid_otp"],
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_failure(message=error_msg["invalid_otp"])

        if not is_validation_time_within_30_minutes(customer_details['mobile']['otp_ts']):
            logger.info(msg=error_msg["otp_expired"],
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_failure(message=error_msg["otp_expired"])

        bo_client_details = COL_CLIENT_DETAILS.find_one({"mobile_no": str(obj.mobile)})
        if back_office_check(field_type='MOBILE', data=obj.mobile):
            data = {"next_stage": EKYC_STAGE_APPROVED,
                    "access_token": "",
                    "client_code": bo_client_details.get('client_code', '') if bo_client_details else '',
                    "completed_stages": ""
                    }
            logger.info(msg="Mobile already exists",
                        extra=get_extra_values(obj.mobile, log_vals, data=data))
            return api_response.common_success(message="Mobile already exists",
                                               data=data)
        if customer_details['email']['is_verified']:
            stage_name = get_next_stage(customer_details['stages'])
        else:
            customer_otp_update = {
                "$set": {
                    "application_no": get_next_application_number(),
                    "event_ts.created_ts": convert_datetime_ist(datetime.utcnow()),
                    "source.id": obj.ref_source,
                    "source.source_id": obj.ref_code,
                    "ekyc_logs.mobile_verified_ts": convert_datetime_ist(datetime.utcnow()),
                    "event_ts.last_login": convert_datetime_ist(datetime.utcnow()),
                    "bool_vals.is_deleted": False
                }
            }
            db_resp = COL_EKYC.update_one({"_id": customer_details['_id']}, customer_otp_update)
            stage_name = 'get_email_otp'
        client_id = str(customer_details['_id'])
        access_token = create_access_token({'client_id': client_id})
        customer_ll_update = {
            "$set": {
                "event_ts.last_login": convert_datetime_ist(datetime.utcnow()),
                "bool_vals.is_relogin_after_delete": True if customer_details['bool_vals']['is_deleted'] else False,
                "bool_vals.is_deleted": False,
                "bool_vals.is_missed_followup": True
            }
        }
        db_resp_ll = COL_EKYC.update_one({"_id": customer_details['_id']}, customer_ll_update)

        resp_data = {"next_stage": stage_name,
                     "access_token": access_token,
                     "completed_stages": get_complete_stages(customer_details['stages'])
                     }
        logger.info(msg="Mobile verification success",
                    extra=get_extra_values(obj.mobile, log_vals, data=resp_data))
        return api_response.common_success(message="Mobile verification success",
                                           data=resp_data)
    except Exception as e:
        logger.error(msg=str(e),
                     extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
        return api_response.internal_error()
