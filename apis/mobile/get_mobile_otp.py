from . import *
from common_functions.enotifiers import e_notifiers


class MobileOTP(BaseModel):
    mobile: str
    device_type: str


err_map = {
    'mobile_exists': 'Mobile already exists.'
}


@app.post(f"{EKYC_BASE_ENDPOINT}verify/mobile/getotp/", tags=["verification"])
# @set_log_details
@set_response
async def generate_mobile_otp(request: Request, response: Response, obj: MobileOTP, api_response=None,
                              log_vals=LOG_MOBILE_GET_OTP):
    try:
        def get_last_accessed_obj():
            return {
                "device_type": obj.device_type,
                "time_stamp": convert_datetime_ist(datetime.now())
            }

        if not is_valid_mobile_number(obj.mobile):
            logger.info(msg="Invalid mobile number",
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_failure(message="Invalid mobile number")

        mobile_otp = get_random_number()
        mobile_details = COL_EKYC.find_one({"mobile.number": obj.mobile}, {"mobile.number": 1, "_id": 1})
        if not mobile_details:
            customer_details_obj = COL_ONBOARDING_MASTER.find_one(
                {'doc_type': 'ekyc_client_structure'}
            )
            customer_details_obj['mobile']['number'] = obj.mobile
            customer_details_obj['mobile']['otp'] = mobile_otp
            customer_details_obj['mobile']['otp_ts'] = convert_datetime_ist(datetime.now())
            customer_details_obj['last_accessed'] = [get_last_accessed_obj()]
            customer_details_obj.pop('_id')
            db_resp = COL_EKYC.insert_one(document=customer_details_obj)
        else:
            customer_otp_update = {
                "$set": {
                    "mobile.otp": mobile_otp,
                    "mobile.otp_ts": convert_datetime_ist(datetime.now())
                },
                "$push": {
                    "last_accessed": get_last_accessed_obj()
                }

            }
            db_resp = COL_EKYC.update_one({"_id": ObjectId(mobile_details['_id'])}, customer_otp_update)
        if not db_resp or not db_resp.acknowledged:
            logger.info(msg="Failed to update the details in the database",
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_failure(message="Failed to update")
        sms_val = {
            'mobile': obj.mobile,
            'mobile_otp': mobile_otp
        }
        sms_status = e_notifiers.send_sms(sms_val, log_vals = log_vals)
        if sms_status == 'sms_sent_success':
            data = {
                "next_stage": "confirm_mobile_otp"
            }
            logger.info(msg="OTP sent successfully to your mobile number",
                        extra=get_extra_values(obj.mobile, log_vals, data=data))
            return api_response.common_success(message="OTP sent successfully to your mobile number",
                                               data=data
                                               )
        else:
            logger.info(msg="Failed to send SMS",
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_failure(message="Failed to send SMS")
    except Exception as e:
        logger.error(msg=str(e),
                     extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
        return api_response.internal_error()
