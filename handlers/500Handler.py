from utils.makeResponse import returnRenderedTemplate

def Handler(requestHeaders):
    return returnRenderedTemplate("WEngine/defaultPages/500.html", {}, 500)