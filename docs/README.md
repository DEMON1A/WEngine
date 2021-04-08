# makeResponse Function
- In the utils. there's a functions called makeResponse used to return the response to the server. in this case there's multiple functions inside of it:
- **returnHTTPBasicResponse** - **Return a static content to the client from the server**
- **returnBasicFileContent** - **Read a local file from the disk then return it's content to the client**
- **returnRenderedTemplate** - **Use the template engine to parse the template and return the response to the client**

### Examples:
- returnHTTPBasicResponse
```python
from utils.makeResponse import returnHTTPBasicResponse

def Handler(requestHeaders):
    return returnBasicHTTPResponse(f'Your ip address is: {requestHeaders['client-ip']}', {}, 200)
```

- returnBasicFileContent
```python
from utils.makeResponse import returnBasicFileContent

def Handler(requestHeaders):
    return returnBasicFileContent("index.html", {}, 200)
```

- returnRenderedTemplate
```python
from utils.makeResponse import returnRenderedTemplate

def Handler(requestHeaders):
    return returnRenderedTemplate("index.html", {}, 200, {"name":"user"})
```

# Dealing with request headers
- WEngine allows you to access the request headers and information via a dict getting passing into your handler function. all of your headers names are in lower case, and if the header doesn't exists then the function will return an error and i guess you know how to deal with dicts. but there's a special headers on the request headers like `client-ip` that you can use to grap the user IP address and `request-method` that's used to grab the request method

### Examples:
- Client-IP
```python
from utils.makeResponse import returnHTTPBasicResponse

def Handler(requestHeaders):
    return returnBasicHTTPResponse(f'Your ip address is: {requestHeaders['client-ip']}', {}, 200)
```

- Request-Method
```python
from utils.makeResponse import returnHTTPBasicResponse

def Handler(requestHeaders):
    return returnBasicHTTPResponse(f'Request Method: {requestHeaders['request-method']}', {}, 200)
```

- Otherwise you can grab other headers on the request like `user-agent` or any other header
```python
from utils.makeResponse import returnHTTPBasicResponse

def Handler(requestHeaders):
    return returnBasicHTTPResponse(f'User-agent: {requestHeaders['user-agent']}', {}, 200)
```

# Creating a route
- To create a route for your application. you need a very basic steps. first of all you should go to `config/routes.py` then add a new value on the dict with your route and it's python handler name. for example you want to add `/test` route. so you go to `config/routes.py` and modify `routes` variables to add into it another value called: `"/test": "testHandler.py"`. after that. you should go to `handlers` folder then create a file called `testHandler.py`. after that you should import the `makeResponse` function from the `utils` folder then use the function you need. let's say you have a template that should return the date. so you should use `returnRenderedTemplate` function on your code then add the filename, response headers, response code, and the variables dict if there is.

# Template Engine
- In WEngine, it uses it's own template engine that have it's own syntax on the code. the first thing you should know here is that every syntax you're adding should end with `,` or your syntax won't be parsed by the template engine. that can cause problems with your code and mess up with the parsing processes.

- On WEngine, there's two template syntax. the first one if `{- variableName -},` that's used to pass variables from your handler into the template content. that means if you passed a variable called `variableName` that does have a value `test`. the template will return `test` word on the page.

- The second template syntax on WEngine is the functions syntax. WEngine template engnine comes with a pre-made functions you can use inside of your template, to use the functions you should use this syntax `{{ function_name() }},`, and the result of the template function should be added into the HTML page on the response

# TE Functions
- In the template engine. there's many functions you can use on your code. that includes but not limited to this functions list:

```
url_to
exec
system
removetags
removeqoutes
markdown
securemarkdown
readfile
base64
base32
date
time
urlencode
```

# TE Functions Usage
- **url_to** - **Adding a path into a web route inside of your application**
- **exec** - **Execute a python code on your server without any output**
- **system** - **Execute system commands on the server and return the output**
- **removetags** - **Remove HTML tags from the string and return the output**
- **removeqoutes** - **Remove qoutes from the string and return the output**
- **markdown** - **Parse the string markdown into HTML with insecure way**
- **securemarkdown** - **Parse the string markdown into HTML with filtering the string before parsing**
- **readfile** - **Return a local file content from the server**
- **base64** - **Base64 encode the string and return the output**
- **base32** - **Base32 encode the string and return the output**
- **date** - **Return the current date**
- **time** - **Return the current time**
- **urlencode** - **URLencode the string and return it on the response**

# TE Functions Arguments
- Before moving into TE arguments. you should know that. functions in the template engine should be seperated using `:` not `,`. because that can result in some issues with the parser. for example in **url_to** calling. you should use something like this: `{{ url_to('static': 'js/code.js') }},`.

### url_to:
- Modes: `static, url, url_base`.
- In this function you should use two arguments. the first one should be the path mode, and the second one should be the path inside of that mode. there's three modes inside of the url_to function. static, that takes the `STATIC_PATH` from the settings. then add the second argument into it. url, that doesn't do anything it just takes the second argument then use it as a path. and the browser should understand that it's from the current domain. url_base, that takes the `SERVER_BASE` path from the settings then add the second argument path into it and return it to the response.

### exec and system
- Both of these functions takes one argument. this argument is used to execute python/cmds on the server and you can't pass any user controlled variables into it. it's just static.

### removetags
- It takes a user controlled variables from the handler then remove the tags from it and reutrn the replaced string

### removeqoutes
- It takes a user controlled variables from the handler then remove the qoutes from it and reutrn the replaced string

### markdown
- It takes a user controlled vairable then parse it with markdown and reutrn it on the response.

### securemarkdown
- It takes a user controlled vairable then parse it with markdown and reutrn it on the response with a secure way and XSS filters inside of it.

### readfile
- It takes a static argument from the template then read it's content and return the file content on the response.
