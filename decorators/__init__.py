import json
from starlette.requests import Request


def generate_curl(method, url, headers=None, body=None):
    curl_parts = ["curl", f"-X {method.upper()}", f'"{url}"']

    if headers:
        # Remove content-length from headers if it exists
        headers = {k: v for k, v in headers.items() if k.lower() != "content-length"}
        for key, value in headers.items():
            curl_parts.append(f'-H "{key}: {value}"')

    if body:
        if isinstance(body, dict):
            body_str = json.dumps(body)
        else:
            body_str = body
        curl_parts.append(f"-d '{body_str}'")

    # Join parts into a single curl command
    return " ".join(curl_parts)

async def get_curl(request: Request):
    method = request.method
    url = str(request.url)
    headers = dict(request.headers)
    body = await request.json() if request.method in ["POST", "PUT"] else None
    return generate_curl(method, url, headers, body)