from config.settings import X_POWERED_BY
from config.settings import FRAME_OPTIONS
from config.settings import CORS_ENABLED
from config.settings import CORS_ORIGIN
from config.settings import CORS_CREDENTIALS
from config.settings import XSS_PROTECTION_HEADER
from config.settings import XSS_PROTECTION_MODE
from config.settings import XSS_PROTECTION_REPORT_URI

from __GLOBAL__ import __NAME__, __VERSION__

def buildHeaders():
    headersList = {}

    if X_POWERED_BY: headersList['X-Powered-By'] = f"{__NAME__} {__VERSION__}"
    if FRAME_OPTIONS: headersList['X-Frame-Options'] = FRAME_OPTIONS
    if CORS_ENABLED:
        headersList['Access-Control-Allow-Origin'] = CORS_ORIGIN

        if CORS_CREDENTIALS: headersList['Access-Control-Allow-Credentials'] = "true"
        else: headersList['Access-Control-Allow-Credentials'] = "false"

    if XSS_PROTECTION_HEADER:
        if XSS_PROTECTION_MODE and XSS_PROTECTION_REPORT_URI:
            headersList['X-XSS-Protection'] = "1"
        elif XSS_PROTECTION_MODE:
            headersList['X-XSS-Protection'] = f"1; mode={XSS_PROTECTION_MODE}"
        elif XSS_PROTECTION_REPORT_URI:
            headersList['X-XSS-Protection'] = f"1; report={XSS_PROTECTION_REPORT_URI}"
    else:
        headersList['X-XSS-Protection'] = "0"

    for singleHeader,singleValue in headersList.items():
        headersList[singleHeader] = singleValue.replace('\n', '').replace('\r', '')

    return headersList
