import js
import pyscript

__DEBUG__ = True


def toggle_debug(mode=None):
    global __DEBUG__
    
    if mode is not None:
        __DEBUG__ = bool(mode)
    else:
        __DEBUG__ = not __DEBUG__

        
def debug(*args, **kwargs):
    # FIXME: Apparently print() if you don't have a tag with terminal attrib on it works like console.log()
    # without the need to use to_js()
    global __DEBUG__
    
    if not __DEBUG__:
        return
    
    if args:
        js.console.log(pyscript.ffi.to_js(args))
    if kwargs:
        js.console.log(pyscript.ffi.to_js(kwargs))
   

def memoize_args(f):
    cache = {}
    def memoized(*args, **kwargs):
        # we intentionally ignore kwargs
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    
    return memoized
