#!/usr/bin/python3.0
import resetcouch
import kotatsu

class root(kotatsu.Object):
    """Root class for all MOO objects."""
    aliases = []
    owner = 'wizard'

class system(root):
    def connect(self):
        return player()
    def parser(self, parse):
        """put the yellow bird in the clock"""
        # This thing is sort of archaic, but lets us get a basic moo going
        prepositions = ['with','using','at','to','in front of', 'in', 'inside',
                        'into', 'on top of', 'on', 'onto', 'upon', 'out of',
                        'from inside', 'from', 'over', 'through', 'under',
                        'underneath', 'beneath', 'behind', 'beside', 'for',
                        'about', 'is', 'as', 'off', 'off of']
        if parse:
            if parse[0] == ";":
                parse = "eval " + parse[1:]
            elif parse[0] == "'":
                parse = "say " + parse[1:]
            if parse[0] == ":":
                parse = "emote " + parse[1:]
            parse = parse.split()
            preposition = set(prepositions).intersection(set(parse))
            verb = parse[0]
            if preposition:
                preposition = preposition.pop()
                (direct_object, indirect_object) = " ".join(parse[1:]).split(preposition, 1)
            else:
                (verb, direct_object, preposition, indirect_object) = (verb,
                                                                       " ".join(parse[1:]),
                                                                       None,
                                                                       None)
            return (verb, direct_object, preposition, indirect_object)
        else:
            return (None, None, None, None)

class utilities(root):
    """Player usable utilities"""
    def show(self):
        return ''

class thing(root):
    description = ""
    location = None    

class room(thing):
    aliases = ["generic room"]
    exits = []
    description = "You see a generic room. You really shouldn't be here."
    def look(self):
        title = self.__class__.__name__.replace('_', ' ').title()
        return title + '\n\n' + self.description

default_room = room('default_room')
default_room.description = 'This is all there is right now.'
kotatsu.save(default_room)

class player(thing):
    description = "You see a player who should type '@describe me as ...'."
    def look(self):
        return self.description
