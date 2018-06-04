import liteframework.application as App

def GlobalFunction(action_method):
    def wrapper(*args, **kwargs):
        return action_method(*args, **kwargs)

    kw = { action_method.__name__ : action_method }
    App.global_functions.update(**kw)
    return wrapper