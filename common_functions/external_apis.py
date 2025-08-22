def get_redirect_url(base_url, end_path, access_token):
    return f"{base_url}{end_path}?state={access_token}"
