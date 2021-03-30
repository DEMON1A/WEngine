from utils.makeResponse import returnRenderedTemplate

def Handler(requestHeaders):
    return returnRenderedTemplate("WEngine/index.html", {}, 200)