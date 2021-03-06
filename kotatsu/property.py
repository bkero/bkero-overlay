#!/usr/bin/env python
"""Simple dynamic property support."""

def property(function):
    """Represent a function as an object property.

    This is best used as a function decorator:
    @property
    def func():
    ...
    """
    import sys
    keys = 'fget', 'fset', 'fdel'
    func_locals = {'doc':function.__doc__}
    def probeFunc(frame, event, arg):
        if event == 'return':
            locals = frame.f_locals
            func_locals.update(dict((k,locals.get(k)) for k in keys))
            sys.settrace(None)
            return probeFunc
    sys.settrace(probeFunc)
    function()
    return property(**func_locals)
