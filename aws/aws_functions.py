from constants.common_imports import *
from constants.config import settings
from database.mongodb.mongodb_common_functions import get_client_pan


def generate_filename(document_purpose: str, client_id: str):
    file_string = document_purpose + client_id
    md5_hash = hashlib.md5()
    md5_hash.update(file_string.upper().encode('utf-8'))
    md5_hash_hex = md5_hash.hexdigest()
    return md5_hash_hex


def get_aws_file_path(client_id, filename, file_format):
    pan = get_client_pan(client_id)
    return f"{settings.AWS_STORAGE_PATH}{pan}/{filename}.{file_format.split('/')[1].lower()}" if pan != 'no_pan_found' else pan
