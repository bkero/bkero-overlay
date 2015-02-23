#!/usr/bin/python3.0
import resetcouch
from kotatsu import Object, load

#   root
#    |  
#  thing 
#   /    \
#toaster  agent
#   \     /
#animated_toaster

class thing(Object): pass
print(dir(thing))

class animated_toaster(Object): pass
print(dir(animated_toaster))
print(animated_toaster.toast)

a = load('animated_toaster', {'Object':Object})

for each in a:
    print(dir(a[each]))
