import os
from urllib.parse import urlparse

def get_proxy_info():
    proxy_env = os.environ.get('http_proxy') or os.environ.get('https_proxy')
    if proxy_env:
        parsed_proxy = urlparse(proxy_env)
        ip = parsed_proxy.hostname
        port = parsed_proxy.port or "Not specified"
        return f"Proxy enabled: IP = {ip}, Port = {port}"
    return "No proxy configured."