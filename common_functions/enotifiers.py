from . import *
from constants.project_imports import *


class ENotifiers:
    def __init__(self):
        self.client_id = settings.NOTIFIER_CLIENT_ID
        self.client_secret = settings.NOTIFIER_CLIENT_SECRET
        self.notifier_url = settings.NOTIFIER_URL
        self.sms_url = settings.SMS_URL

    def get_email_payload(self, var_vals: dict, sender_email: str, email_name: str, email_temp: str, subject: str):
        return {
            "emailName": email_name,
            "variables": var_vals,
            "to": sender_email,
            "subject": subject,
            "templateName": email_temp,
            "templateCategory": "Firstock_Updated_Content"
        }

    def send_sms(self, value, **kwargs):
        try:
            sms_req = self.sms_url.replace("{#mob#}", value['mobile'])
            sms_req = sms_req.replace("{#otp#}", value['mobile_otp'])
            logger.info(msg='SMS request for sending OTP',
                        extra=get_extra_values(value['mobile'], kwargs.get('log_vals', ''),
                                               data={
                                                   'method': 'get',
                                                   'url': sms_req
                                               }))
            sms_response = requests.get(sms_req)
            logger.info(msg='SMS sent successfully' if sms_response.status_code == 200 else 'SMS OTP not sent',
                        extra=get_extra_values(value['mobile'], kwargs.get('log_vals', ''),
                                               data=sms_response.content.decode('utf-8')))
            return 'sms_sent_success' if sms_response.status_code == 200 else 'sms_sent_failed'
            # value['data']['sms_id'] = json.loads(sms_response.content)['sms_id'].strip()
        except Exception as e:
            logger.error(msg=str(e),
                         extra=get_extra_values(value['mobile'], kwargs.get('log_vals', ''), data=''))
            return 'sms_sent_failed'

    def send_email(self, sender_email: str, subject: str, email_name: str, email_temp: str, var_vals: dict, **kwargs):
        try:
            url = self.notifier_url + "service/emailTemplate/send"
            payload_val = self.get_email_payload(var_vals=var_vals, sender_email=sender_email, email_name=email_name,
                                                 email_temp=email_temp, subject=subject)

            logger.info(msg='Email request for sending OTP',
                        extra=get_extra_values(kwargs.get('client_id', ''), kwargs.get('log_vals', ''),
                                               data={
                                                   'method': 'post',
                                                   'url': url,
                                                   'payload': payload_val,
                                               }))

            email_response = requests.post(url, json=payload_val,
                                           auth=HTTPBasicAuth(self.client_id, self.client_secret))

            logger.info(msg='Email sent successfully' if email_response.status_code == 200 else 'Email OTP not sent',
                        extra=get_extra_values(kwargs.get('client_id', ''), kwargs.get('log_vals', ''),
                                               data=email_response.json()))

            return 'email_sent_success' if email_response.status_code == 200 else 'email_sent_failed'
        except Exception as e:
            logger.error(msg=str(e),
                         extra=get_extra_values(kwargs.get('client_id', ''), kwargs.get('log_vals', ''), data=''))
            return 'email_sent_failed'


e_notifiers = ENotifiers()
