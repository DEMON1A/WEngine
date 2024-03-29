# WEngine (WEB Engine) :dizzy: ![](https://tokei.rs/b1/github/DEMON1A/WEngine)
- WEngine is a web framework written in python allows you to create your own web applications, it's currently still in beta

## What Functions WEngine is Using?
- In WEngine. I wrote everything from zero. it starts with the python server that's written with `http.server` in python. and linked with the user controlled routes to allow the user to set his own routes on the server with it's handler. that controls the content on the response the client is getting. after that WEngine is using **regex** to detect your template syntaxes inside of the HTML code. that allow you to use a pre-made functions inside your HTML template and do back-end functions on the front-end side like reading files, executing commands, passing variables, ..etc

## How WEngine is Working?
- WEngine has built in a hadler system that works on getting the client request data from the python server then return the response the client should get. your handlers should be stored on the `handlers` folder inside of the application so the server can access it and your handler should be a function called `Handler` that takes only one argument called `requestHeaders`. you can include any other python functions on your code to use it inside of the `Handler` function. but you should return a response after running all of this function. otherwise the server won't work

- To return a response, you should be returning three values: `responseContent`, `responseHeaders` and `responseCode`. and all of them shouldn't be empty or decleared with other types. but to make it easy for the user. I created a full function called `makeResponse` in the `utils` folder. that works on returning the response to the server and fill the missing fields and validate it. and it could be used to render templates too. allowing you to use WEngine syntax inside of your HTML file and pass variables to it.

## How requests works inside WEngine?
- Basicly, WEngine is just a set of routes inside a web server, whenever we get a request from the user requesting a specific route, the server attempts to look if this routes exists, if it does it tries to find it's handler and once it does it provides the route handler with the client request info, and takes the response content, response headers and response code from the handler, then returns it to the client

## How To Use WEngine?
- Make sure you read the documentations for WEngine. to avoid adding extra content to the README the documentations has been moved to readthedocs and you should find the link to it under the project description. or you can visit: [https://wengine.readthedocs.io/en/latest/](https://wengine.readthedocs.io/en/latest/). but at the current time. the documentations isn't complete. take a deep look trying to understand how it works.

## Security
- WEngine has been built with a secure way for both the client-side and the server-side. Most of the protections there on the server is managed by the user. you're able to disable it or to enable it. make sure you see `config/settings.py` and modify what won't fit with your application. otherwise that can result in a real security issues on your application.

- WEngine created a protection for most of the functions inside of the on the `utils`. if you want to use something and it does exists on the `utils` folder. please don't create an external function for it. the `utils` functions has been made with a security protections that does fit with your server configurations. using external functions will allow these secrity issues to happen unless you're sure you're validating the code

- But BTW, if you think you found a security issue on WEngine. please [contact me](mailto:mdaif1332@gmail.com) and i will response ASAP. if you didn't notice a response from me. then feel free to submit an issue on github with it.

## What's New?
- Server logs with full details about users requests.
- Clean logs mode to allows users empty the log file.
- New template engine, with bug fixes and fast syntax parsing.
- Public logs viewer to show the logs content on the web server only when it's enabled.
- Full cors system with multiple origins support on the settings.
- Setting/Deleting Cookies support with many security layers to keep it secure
- SQLite3 db interaction that makes it easy to interact with your database using a pre-made util.
- `createuser` and `migrate` options to add new user to the database and setup the SQLite db.

## Collaborators :heart:
- [Mohammed Matar](https://github.com/Micro0x00) - **( WEngine landing page design )**

## Support WEngine
- Giving WEngine a :star: on github will be great. that's the least you can do to support WEngine. and I would be really thankful for that!. You can also support WEngine from the sponser links on the github to help WEngine developers and keep it a maintained project.
