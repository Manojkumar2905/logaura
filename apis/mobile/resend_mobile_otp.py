from constants.common_imports import *
from constants.project_imports import *
from common_functions.enotifiers import e_notifiers


class ResendMobileOTP(BaseModel):
    mobile: str


err_map = {
    'mobile_not_exists': 'Mobile not exists.'
}


@app.post(f"{EKYC_BASE_ENDPOINT}verify/mobile/resend_otp/", tags=["verification"])
@set_log_details
@set_response
async def resend_mobile_otp(request: Request, response: Response, obj: ResendMobileOTP,
                            api_response=None, log_vals = LOG_MOBILE_RESEND_OTP):
    try:
        if not is_valid_mobile_number(obj.mobile):
            logger.info(msg="Invalid mobile number",
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_failure(message="Invalid mobile number.")

        mobile_details = COL_EKYC.find_one({"mobile.number": obj.mobile}, {"mobile.number": 1, "_id": 1})
        if not mobile_details:
            logger.info(msg=err_map['mobile_not_exists'],
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_failure(message=err_map['mobile_not_exists'])

        mobile_otp = get_random_number()
        customer_otp_update = {
            "$set": {
                "mobile.otp": mobile_otp,
                "mobile.otp_ts": convert_datetime_ist(datetime.now())
            }

        }
        db_resp = COL_EKYC.update_one({"_id": ObjectId(mobile_details['_id'])}, customer_otp_update)
        if not db_resp or not db_resp.acknowledged:
            logger.info(msg="Failed to update the details in the database",
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return common_failure(message="Failed to update", api_response=api_response)

        sms_val = {
            'mobile': obj.mobile,
            'mobile_otp': mobile_otp
        }

        sms_status = e_notifiers.send_sms(sms_val, log_vals = log_vals)
        if sms_status == 'sms_sent_success':
            logger.info(msg="OTP resent successfully to your mobile number",
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_success(message="OTP sent successfully to your mobile number")
        else:
            logger.info(msg="Failed to send SMS",
                        extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
            return api_response.common_failure(message="Failed to send SMS")
    except Exception as e:
        logger.error(msg=str(e),
                     extra=get_extra_values(obj.mobile, log_vals, data=obj.model_dump()))
        return api_response.internal_error()
