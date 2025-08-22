"""Mobile"""
try:
    from ekyc.V1.mobile.get_mobile_otp import *
except Exception as e:
    print(f"Error in the V1 version get_mobile_otp ->{e}")

try:
    from ekyc.V1.mobile.verify_mobile_otp import *
except Exception as e:
    print(f"Error in the V1 version verify_mobile_otp ->{e}")

try:
    from ekyc.V1.mobile.resend_mobile_otp import *
except Exception as e:
    print(f"Error in the V1 version resend_mobile_otp ->{e}")

"""Email"""

try:
    from ekyc.V1.email.get_email_otp import *
except Exception as e:
    print(f"Error in the V1 version get_email_otp ->{e}")

try:
    from ekyc.V1.email.verify_email_otp import *
except Exception as e:
    print(f"Error in the V1 version verify_email_otp ->{e}")

try:
    from ekyc.V1.email.resend_email_otp import *
except Exception as e:
    print(f"Error in the V1 version resend_email_otp ->{e}")


try:
    from ekyc.V1.email.verify_email_by_google import *
except Exception as e:
    print(f"Error in the V1 version verify_email_by_google ->{e}")
