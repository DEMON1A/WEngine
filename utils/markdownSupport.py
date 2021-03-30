import markdown
import re

def createMarkdown(mdSyntax):
    htmlContent = markdown.markdown(mdSyntax)
    return htmlContent

def secureMarkdown(mdSyntax):
    '''
    on python markdown. it should be two layers of validation. the first one for HTML
    tags to check if the user added any kind of HTML tags that doesn't belong to markdown.
    that can result in a XSS in this case.

    the other validation should be about the URLs inside of the application. and if there's any URL that
    contains `javascript:` scheme. because that can result in a XSS too

    avoid using markdown outside of these functions. WEngine does offer you the security protections. but
    it can't help you when you're using an exteral functions on your code.
    '''

    htmlTags = re.findall(r"\<.*\>", mdSyntax)
    if len(htmlTags) != 0:
        for singleTag in htmlTags:
            nMdSyntax = mdSyntax.replace(singleTag, '')
    else:
        nMdSyntax = mdSyntax

    JSurls = re.search(r"\]\(javascript\:", nMdSyntax.lower())
    if JSurls != None:
        replaceString = JSurls.group()
        realMdSyntax = nMdSyntax.lower().replace(replaceString, '](https://')
    else:
        realMdSyntax = nMdSyntax

    htmlContent = markdown.markdown(realMdSyntax)
    return htmlContent
    