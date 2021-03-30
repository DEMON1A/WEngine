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

