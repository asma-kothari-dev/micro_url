import base64


class Codec(object):

    def encode(self, value):
        """ Encodes a string to base64 data """
        try:
            encoded = base64.encodestring(value)
        except Exception:
            encoded = None
        return encoded

    def decode(self, value):
        """ Encodes a string to base64 data """
        try:
            decoded = base64.decodestring(value)
        except Exception:
            decoded = None
        return decoded
