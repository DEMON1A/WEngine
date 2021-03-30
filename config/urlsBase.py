'''
this module is used for the `url_to` template function
so users should be able to select between the static modes
inside of this function
'''
from config.settings import SERVER_BASE
from config.settings import STATIC_PATH
from os.path import abspath

urlModes = {
    "url_base": f"/{SERVER_BASE}",
    "url": "",
    "static": f"/{STATIC_PATH}"
}