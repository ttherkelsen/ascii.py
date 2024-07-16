from pyscript import window, ffi, display, HTML
import sys, os

display(HTML("<pre>" + "\n".join(os.listdir("/")) + "</pre>"))
window.console.log(ffi.to_js([ t for t in globals().keys() ]))
window.console.log(repr(sys.path))
window.console.log(repr(os.listdir(".")))
