#!/usr/bin/python3.0
import resetcouch
from kotatsu import Object

a=[]

# Creating the concept of objects
for i in range(1,100):
    s =  Object()
    s.a = []
    for ii in range(1,1000):
        s.a.append(1000)
    a.append(s)
