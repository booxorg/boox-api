# liteframework
A POC Python Web Framework following MVC principles

## General description
Everything starts with Apache receiving a request. `mod_wsgi` executes `index.wsgi` located in the public directory, passing variables `environ` and `start_response` to a function called `application` (defined by the standard [PEP 3333](https://www.python.org/dev/peps/pep-0333/)).
* The `environ` dictionary contains all the information about the request such as `SERVER_PORT`, `REQUEST_METHOD`, `SERVER_PROTOCOL`, `CONTENT_LENGTH`, `HTTP_USER_AGENT` and others.
* The `start_response` is a callable used to begin the HTTP response. [Docs here](https://www.python.org/dev/peps/pep-0333/#the-start-response-callable)

From now on, our framework is in controll and is responsible for returning the response headers and content.
The `application` function in `index.wsgi` sets up global Application variables like `request_url`, `base_path`, `public_path` and builds the Request object that will be passed along to controllers.

### Global Application Variables
```
import liteframework.application as App
print(App.environ)
```
| Name              | Description                                                                           |
|-------------------|---------------------------------------------------------------------------------------|
| environ           | The original dictionary received from Apache                                          |
| start_response    | The original callable function to start the HTTP response                             |
| base_path         | The root path of the application, essentially the project folder                      |
| public_path       | The path to the `public` directory                                                    |
| app_path          | The path to the `app` directory                                                       |
| resources_path    | The path to the `resources` directory                                                 | 
| views_path        | The path to `resources/views` directory                                               |
| global_functions  | Internal object, contains all the global functions declared by the framework and user |
| jinja_env         | The enviroment object of the template engine [Jinja](http://jinja.pocoo.org/)         |
| routing_table     | Contains all the information about the user defined routes                            |

### Request Object 
Gets created and passed to every defined route with the name `request`
Contains the following fields, that are accessed in the following manner 
```
request.protocol
request.request_scheme
```
| Name | Description |
|------|-------------|
| port | The port that was used to make the request, equivalent with `SERVER_PORT` |
| protocol | Usually is `HTTP/1.1`, denotes the communication protocol |
| content_length | The contents of any Content-Length fields in the HTTP request. If absent - the value will be zero |
| user_agent | The request user agent |
| request_scheme | `http` or `https` |
| remote_port | The remote port from which the request was made |
| lang | Language headers, might look something like that `en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7`
| content_type | The contents of any Content-Type fields in the HTTP request. If absent `text/html` is considered |
| accept_encoding | The encoding the user accepts as a response, might look something like this `gzip, deflate, br`
| method | `GET`, `POST`, `PUT` and others |
| url | Relative url starting from the root; `/index`, `/test/value` are some examples
| input | Form input, if given |  

# What happens next
After the `Application` and `Request` have been initialized, the `Router` takes control.