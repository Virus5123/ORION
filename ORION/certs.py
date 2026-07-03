import ssl
import certifi

def get_cert():
    context = ssl.create_default_context()
    context.load_verify_locations(certifi.where())
    return context