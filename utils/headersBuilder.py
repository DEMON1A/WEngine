'''
this util is made to read and seprate the http headers that came
from the client-side so the handlers can use it on their own modules
and build what they need with it
'''

def bHeaders(Headers):
    realHeaders = {}

    Headers = str(Headers)
    headersList = Headers.split('\n')

    for singleHeader in headersList:
        if singleHeader != "":
            headerContent = singleHeader.split(":", maxsplit=1)

            headerName = headerContent[0].strip().lower()
            headerValue = headerContent[1].strip()

            realHeaders[headerName] = headerValue
        else:
            pass

    return realHeaders