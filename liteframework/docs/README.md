# liteframework
A POC Python Web Framework following MVC principles

## Disclaimer 
This is a POC Framework that doesn't in any way claim to be secure or correct. It does not and will never guarantee compatibility or reliability and exists purely for educational purposes.

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
| cookies_pub       | The public RSA1024 key for cookie encryption, gets loaded from `storage/keys/cookie_public.pem` |
| cookies_prv       | The private RSA1024 key for cookie decryption, gets loaded from `storage/keys/cookie_private.pem` |
| config            | The [ConfigParser](https://docs.python.org/2/library/configparser.html) object, that holds the application configuration read from `config.ini` |
| session           | Session object that gets created (or loaded) on each request |

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
| cookies | Cookie values read from the `HTTP_COOKIE` header |
| new_cookies | New cookie values that will be set during the runtime of the application. Will be sent to the user with the `Set-Cookie` header |
| params | Python dictionary holding the `GET` parameter `(key, value)` pairs
| url_no_params | The request url without get parameters, for internal use in matching |

# What happens next
After the `Application` and `Request` have been initialized, the `Router` takes control.
It will iterate through all the defined routes (the function `route_url` inside `liteframework/routing.py`) and will try to match one of them. After it succeeds, the subsequent controller method will be called.
### Declaring a route
Routes are declared inside `app/controllers` folder. All the related or dependent routes should be placed in the same controller. The route `register` and `register_post` might be placed together in `register_controller.py`. This is the convention, but there are not limits to the number or naming of the controllers as they all are imported by the application.
_Obviously, all the files in the `controllers` folder _must_ have controller functionality_
```
import liteframework.controller as Controller 
import liteframework.routing as Routing 

@Routing.Route(url='/', method='GET')
def index(variables={}, request={}):
    return Controller.response_data('This is a test route')
```
The decorator `Routing.Route` binds the given url template to the declared function. As soon as any request matches the template - the given function will be called.

#### Routing.Route params

| Name | Description | Type |
|------|-------------|------|
| url | The template url to be matched, has a specific format which is described below | String |
| method | `GET`, `POST`, `PUT`, `DELETE` may be used, only the matching requests will be redirected to the function | String |
| middleware | Contains the list with names of the middleware to be called before the function, but after the match | List |
| disabled | Boolean value that activates/deactivates the route | Boolean |

#### Template format
A template should be _relative_, from the root, for example `/main`, `/user/id`, `/profile`
Optionally, a template allows variables in the following format `{<variable_name>::<variable_regex>}`
1. `<variable_name>` is how it will be named and passed along to the controller, for example `user_id`, `page_id`, etc.
2. `<variable_regex>` is the python regex that should match the variable, for example `\d\d` will match two digits, `[A-Z]{1, 5}` will match a string containing letters from A to Z from 1 to max 5 times.

Some variable examples are 
1. `{name::[A-Za-z]+}`
2. `{id::[0-9]+}`

A template can contain an indefinite number of variables with **unique** names.
1. `/user/{id::[0-9]{10}}/profile`
2. `/product/{name::[A-Za-z_-]+}`

**All the variables will be passed along to the controller in the `variables` dictionary having their names as keys.**


### Cookies
```
import liteframework.cookies as Cookies
Cookies.set_cookie(request, 'name', 'John Doe', expires_after_days=60)
name = Cookies.get_cookie(request, 'name', 'Unknown name')
```
The framework supports a very primitive version of cookies.
They are encrypted with `1024 bit RSA` and stored in the user's browser for 30 days but default or for  `expires_after_days`.
The encryption keys are genereated an stored as `/storage/keys/cookie_private.pem` and `/storage/keys/cookie_public.pem`.
1. When the user sends an request, the script checks for the existence of the header `HTTP-COOKIE`, which will be parsed and
kept in `request.cookies` internal object. 
2. When the user asks for a cookie, its value is extracted from the object and decrypted with the private key.
3. When the user stores a cookie, it gets encrypted with the public key and saved in `request.new_cookies` and then added to the response as a `Set-Cookie` header 

The current cookie functions are 

#### set_cookie

| Name | Description |
|------|-------------|
| request               | _Mandatory parameter_, the received request object |
| key                   | _Mandatory parameter_ The cookie name |
| value                 | _Mandatory parameter_ The cookie value (will be encrypted) |
| path                  | Cookie path    |
| expires_after_days    | Number of days for the cookie to live |
| domain                | Cookie domain |

#### get_cookie

| Name | Description |
|------|-------------|
| request               | _Mandatory parameter_, the received request object |
| key                   | _Mandatory parameter_ The cookie name |
| default               | _Mandatory parameter_ The cookie default value if it's not found |

#### delete_cookie
Will invalidate the cookie by setting expire date to past

| Name | Description |
|------|-------------|
| request               | _Mandatory parameter_, the received request object |
| key                   | _Mandatory parameter_ The cookie name |

### Installation

1. `sudo apt-get update`

2. Install apache
`sudo apt-get install apache2 apache2-utils libexpat1 ssl-cert python`

3. Install mod-wsgi
`sudo apt-get install libapache2-mod-wsgi`

4. Restart apache
`sudo /etc/init.d/apache2 restart`

5. Add the config (with a proper name, and chaning all the names in the conf)
`cp docs/defaults/000-default.conf /etc/apache2/sites-available/project.conf`

6. Enable the site
`sudo a2ensite project.conf`

7. Reload apache
`sudo service apache2 reload`

8. Install mysql

    ```
    sudo apt-get install mysql-server
    sudo apt-get install python-pip python-dev libmysqlclient-dev
    sudo pip install MySQL-python
    ```

9. Create the database and tables

10. Copy the default `docs/defaults/config.ini` to the root and change all the necessary variables 
 
11. Enjoy
