from constants.common_imports import *
from constants.config import settings


class AwsConnectivity:
    def __init__(self,
                 bucket_name=settings.AWS_BUCKET_NAME,
                 aws_access_key_id=settings.AWS_ACCESS_KEY,
                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                 region=settings.AWS_REGION,
                 aws_service='s3',
                 aws_request='aws4_request',
                 exp_duration=settings.AWS_EXPIRY_DURATION,
                 role_arn=settings.AWS_ROLE_ARN
                 ):
        self.bucket_name = bucket_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region
        self.aws_service = aws_service
        self.aws_request = aws_request
        self.exp_duration = exp_duration
        self.role_arn = role_arn
        self.mo_base_url = settings.MO_BASE_URL

    def get_metadata(self, file_name):
        metadata_key_value = "x-amz-meta-auth"
        encrypt_data_text = (self.bucket_name +
                             self.aws_access_key_id +
                             self.aws_secret_access_key +
                             self.region +
                             file_name +
                             settings.AES_SECRET)
        return {metadata_key_value: hashlib.sha256(encrypt_data_text.encode()).hexdigest()}

    def mo_api(self, function_type, aws_path: str, file: bytes = None,
               metadata: dict = {}):
        mo_url = f"{self.mo_base_url}aws/{function_type}"
        try:
            file_name, file_format = aws_path.rsplit(".", 1)
            file_name = file_name.rsplit("/", 1)[1]
        except Exception as e:
            return 400, "split_aws_path_error"
        mo_payload = {
            'bucket_name': self.bucket_name,
            'access_key': self.aws_access_key_id,
            'secret_access_key': self.aws_secret_access_key,
            'region': self.region,
            'expiry_duration': self.exp_duration,
            'role_arn': self.role_arn,
            'aws_path': aws_path,
            'metadata': json.dumps(self.get_metadata(file_name=file_name))
        }
        if function_type == 'upload_document':
            files = {
                'file': (file_name, file)
            }
            mo_resp = requests.post(mo_url, data=mo_payload, files=files)
        else:
            mo_resp = requests.post(mo_url, json=mo_payload)

        return mo_resp.status_code, mo_resp.json()

    def upload_document(self, file: bytes, aws_path: str):
        return self.mo_api(function_type='upload_document', aws_path=aws_path, file=file)

    def delete_document(self, aws_path: str):
        return self.mo_api(function_type='delete_document', aws_path=aws_path)

    def get_doc_url(self, aws_path: str):
        return self.mo_api(function_type='get_doc_url', aws_path=aws_path)
