####################################################################################
####
####    This module holds the main information about the paths and environmental 
####    variables. 
####    It gets instantiated at the very start of the request, in the public/index.wsgi
####    To use paths, env and start_response function - import this module
####    import liteframework.application as App
####    and access members
####    App.public_path, App.jinja_env
####
####################################################################################

environ = None
start_response = None
base_path = None 
public_path = None
app_path = None
resources_path = None
views_path = None
global_functions = {}
jinja_env = None
routing_table = {}


