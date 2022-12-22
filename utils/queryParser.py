from urllib.parse import urlparse

def parseQuery(path):
    parsedObject = urlparse(path)
    if parsedObject.query == '':
        return {}
    else:
        parametersList = {}
        query = parsedObject.query

        if "&" in query:
            query = query.split('&')
            for item in query:
                if "=" in item:
                    i = item.split('=', maxsplit=1)
                    parametersList[i[0]] = i[1]
                else:
                    parametersList[item] = ''
        else:
            if "=" in query:
                query = query.split('=', maxsplit=1)
                parametersList[query[0]] = query[1]
            else:
                parametersList[query] = ''

        return parametersList

def parsePath(path):
    return urlparse(path).path