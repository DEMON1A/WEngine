'''
this controller is created to hanlde the requests into the web server
then validate the origin header. and response with the common cors stuff
'''
from config.settings import CORS_ORIGIN
from utils.showMessage import showError

def corsOrigin(requestHeaders):
    if type(CORS_ORIGIN) == str:
        try:
            originHeader = requestHeaders['origin']
            if not originHeader.strip().startswith('http://') and not originHeader.strip().startswith('https://'):
                if validateCors(originHeader, CORS_ORIGIN):
                    originHeader = f"http://{originHeader.strip()}/"
                    return originHeader
                else:
                    originHeader = f"http://{CORS_ORIGIN.strip()}/"
                    return originHeader
            else:
                if validateCors(originHeader, CORS_ORIGIN):
                    originHeader = originHeader.strip()
                    return originHeader
                else:
                    originHeader = CORS_ORIGIN.strip()
                    return originHeader
        except Exception:
            # there's no origin header. default one is the one on the server
            # so we need to use the config from here
            if not CORS_ORIGIN.strip().startswith('http://') and not CORS_ORIGIN.strip().startswith('https://'):
                originHeader = f"http://{CORS_ORIGIN.strip()}/"
                return originHeader
            else:
                originHeader = originHeader.strip()
                return originHeader
    elif type(CORS_ORIGIN) == list:
        # there's a full list of cors in thus case
        # two validations are required here, can't use the old method
        # string validation then validateCors function.
        try:
            originHeader = requestHeaders['origin']
            for singleOrigin in CORS_ORIGIN:
                if validateCors(originHeader, singleOrigin):
                    if not originHeader.strip().startswith('http://') and not originHeader.strip().startswith('https://'):
                        originHeader = originHeader.strip()
                        originHeader = f"http://{originHeader}/"
                        return originHeader
                    else:
                        originHeader = originHeader.strip()
                        return originHeader
                else:
                    pass

            originHeader = CORS_ORIGIN[0].strip()
            if not originHeader.startswith('http://') and not originHeader.startswith('https://'):
                originHeader = f"http://{originHeader}/"
                return originHeader
            else:
                originHeader = originHeader
                return originHeader            
        except Exception:
            originHeader = CORS_ORIGIN[0].strip()
            if not originHeader.startswith('http://') and not originHeader.startswith('https://'):
                originHeader = f"http://{originHeader}/"
                return originHeader
            else:
                originHeader = originHeader
                return originHeader
    else:
        showError(exceptionRule="Config Error", Message="Invalid Cors origin on the settings, it can't be bool/int/float only str and list")

# should i use some re validation here?
def validateCors(Origin, cOrigin):
    Origin = Origin.replace('https://', '').replace('http://', '')
    originHost = Origin.split('.')

    if len(originHost) > 2:
        # there's a subdomain on the origin
        mainHost = originHost[-2:]
        replaceHost = '.'.join(originHost)
        mainHost = '.'.join(mainHost)

        Origin = Origin.replace(replaceHost, mainHost)

    NewOrigin = Origin[:len(cOrigin)]
    replaceString = Origin.replace(NewOrigin, '')

    if NewOrigin == cOrigin:
        if not replaceString.strip().startswith('/') and not replaceString.strip() == "": return False
        else: return True
    else:
        return False
