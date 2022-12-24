'''
this util is created to validate routes getting created using the CLI 
tool and verify the routes that does exist aswell to avoid using some
characters on the routes, as long as an LFI protection for the routes
paths
'''

from string import ascii_letters
from string import digits

def validateRoute(routeName):
    CHARS = ascii_letters + digits + "$-_<>!@$%*&()+/"
    for singleChar in routeName:
        if singleChar not in CHARS:
            return False

    return True

def validatePath(routePath):
    if "../" in routePath or "..\\" in routePath:
        return routePath.replace('..', '')