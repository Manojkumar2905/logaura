import datetime

from . import *

ist_format = pytz.timezone('Asia/Kolkata')

def convert_datetime_ist(date_time):
    return date_time + timedelta(hours=5, minutes=30)


def check_required_key(class_inst, required_keys: tuple):
    for key in required_keys:
        return key if not getattr(class_inst, key, None) else "all_keys_available"


def is_valid_string(str_val, min_val=3, max_val=50):
    return True if min_val <= len(str_val) <= max_val else False


def to_dict(obj):
    result = {}
    for attr_name in obj.__dict__:
        result[attr_name] = "value_" + str(getattr(obj, attr_name))
    return result


def is_valid_uuid(uuid_string):
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False


def is_validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_mobile_number(number):
    pattern = r'^(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}$'
    return re.match(pattern, number) is not None


def valid_10_digit_phone_number(phone):
    phone = re.sub(r'^\+?91', '', phone)
    return phone[-10:]


def is_validate_date(date_string):
    pattern = re.compile(r'^\d{4}/\d{2}/\d{2}$')
    return True if pattern.match(date_string) else False


def is_date_less_than_min_date(date_str, min_date):
    try:
        year, month, day = map(int, date_str.split('/'))
        min_year, min_month, min_day = map(int, min_date.split('/'))
        if year < min_year:
            return True
        elif year == min_year and (month < min_month or (month == min_month and day < min_day)):
            return True
        else:
            return False
    except ValueError:
        return False


def is_valid_png_base64(base64_string: str):
    try:
        img = Image.open(BytesIO(base64.b64decode(base64_string)))
        if img.format == 'PNG':
            return True
        else:
            return False
    except Exception as e:
        return False


def validate_aadhaar(aadhaar_number):
    aadhaar_pattern = re.compile(r'^[0-9]{12}$')
    return True if aadhaar_pattern.match(aadhaar_number) else False


def validate_pan(pan_number):
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    return True if re.match(pattern, pan_number) else False


def calculate_age(dob):
    # today = datetime.today()
    today = convert_datetime_ist(datetime.now())
    born = get_date_from_string(dob)
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def get_date_from_string(val):
    # return datetime.strptime(val, '%Y/%m/%d')
    return datetime.strptime(val, "%Y/%m/%d").replace(tzinfo=timezone.utc).astimezone(ist_format)


def get_random_number(length: int = 6):
    return f"{random.randint(1, 999999):06}"


def is_validation_time_within_30_minutes(expiry: datetime) -> bool:
    current_time = convert_datetime_ist(datetime.utcnow())
    time_difference = current_time - expiry
    if timedelta(minutes=0) <= time_difference <= timedelta(minutes=30):
        return True
    return False


def mask_value(mask_val, mask_char="*"):
    if not isinstance(mask_val, str):
        mask_val = str(mask_val)

    if not mask_val:
        return ""

    result = []
    i = 0
    length = len(mask_val)

    while i < length:
        for j in range(min(3, length - i)):
            result.append(mask_char)
            i += 1
        for j in range(min(2, length - i)):
            result.append(mask_val[i])
            i += 1
    return "".join(result)


def convert_class_to_dict(obj):
    # attributes = {}
    # for attr in dir(obj):
    #     # Filter out special methods if needed
    #     if not attr.startswith('__'):
    #         attributes[attr] = getattr(obj, attr)
    # return attributes
    try:
        # First attempt: using vars() which works for most custom classes
        return vars(obj)
    except TypeError:
        try:
            # Second attempt: using __dict__ directly
            return obj.__dict__
        except (AttributeError, TypeError):
            try:
                # Third attempt: use dir() and getattr() for objects
                # that don't expose __dict__ directly
                result = {}
                for attr in dir(obj):
                    # Skip magic methods and callable methods
                    if not attr.startswith('__') and not callable(getattr(obj, attr)):
                        result[attr] = getattr(obj, attr)
                return result
            except Exception:
                # Last resort: if nothing works, return empty dict
                return {}