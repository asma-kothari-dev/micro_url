import base64


def encode(value):
    """ Encode a string using Base64 """
    try:
        encoded = base64.b64encode(value)
    except Exception:
        encoded = None
    return encoded


def decode(self, value):
    """ Decode a Base64 encoded string """
    try:
        decoded = base64.b64decode(value)
    except Exception:
        decoded = None
    return decoded
