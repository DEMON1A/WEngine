import base64

def base64Encode(encodeString):
    encodeString = encodeString.encode('UTF-8')
    encodeString = base64.b64encode(encodeString)
    encodeString = encodeString.decode('UTF-8')

    return encodeString

def base32Encode(encodeString):
    encodeString - encodeString.encode('UTF-8')
    encodeString = base64.b32encode(enocdeString)
    encodeString = encodeString.decode('UTF-8')

    return encodeString