#!/usr/bin/python3.0
import resetcouch
from kotatsu import Object

#   root
#    |  
#  thing 
#   /    \
#toaster  agent
#   \     /
#animated_toaster

class thing(Object):
    location = 'here'

class agent(thing):
    name = 'Robert'
        
class toaster(thing):
    description = "Bread to toast conversion entity."

class animated_toaster(toaster, agent):
    name = 'Queen of france'
    description = 'animated!'
    def toast(self):
        return "This is a verb."

qof = animated_toaster()
qof.description = 'in color!'
