import js
import pyscript

# Possibly more functionality 

class Core:
    def log(*args, **kwargs):
        if args:
            js.console.log(pyscript.ffi.to_js(args))
        if kwargs:
            js.console.log(pyscript.ffi.to_js(kwargs))
