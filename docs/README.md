# Template Engine
- In WEngine, it uses it's own template engine that have it's own syntax on the code. the first thing you should know here is that every syntax you're adding should end with `,` or your syntax won't be parsed by the template engine. that can cause problems with your code and mess up with the parsing processes.

- On WEngine, there's two template syntax. the first one if `{- variableName -},` that's used to pass variables from your handler into the template content. that means if you passed a variable called `variableName` that does have a value `test`. the template will return `test` word on the page.

- The second template syntax on WEngine is the functions syntax. WEngine template engnine comes with a pre-made functions you can use inside of your template, to use the functions you should use this syntax `{{ function_name() }},`, and the result of the template function should be added into the HTML page on the response

# Template Engine Functions
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

# Templates Engine Functions Usage
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
