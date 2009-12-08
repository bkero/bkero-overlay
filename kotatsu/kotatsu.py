#!/usr/bin/env python
import config
import couch
import base
import types

couch.debug = False
c = couch.Couch(config.couchdb_host)

# When serializing objects, skip these properties
skip_list = ['_id', '_rev', '__module__', 
             '__module__', '__del__', 
             '__getattribute__', '__scope__', 
             '__save__', '__delete__', '__new__']

def create_couch(id = None, type="object", cls=None):
    """Create an initial revision of an object, assigning an id if needed."""
    if type == 'object':
        # Default object attributes
        moo_builtins = '{"value":{}, "type":"' + type + '", "class":"{0}"'.format(cls) + '}'
    elif type == 'class':
        # Default class attributes
        moo_builtins = '{"value":{}, "type":"' + type + '", "parents":{}}'
    else:
        raise Exception('Invalid document type.', type)

    if id: # Explicit id
        return c.saveDoc('moo', moo_builtins, id)['id']
    else: # Implicit (generated couchdb side)
        return c.saveDoc('moo', moo_builtins)['id']

def missing(v):
    """Shorthand for missing couch objects."""
    if 'error' in v and 'reason' in v and v['reason'] == 'missing':
        return True
    else:
        return False

def openorcreate(id, type):
    """Open or create a object/class."""
    v = c.openDoc('moo', id)
    if 'value' not in v:
        if missing(v):
            id = create_couch(id, type)
            v = c.openDoc('moo', id)
    return v

# Metaclass to construct Kotatsu classes and objects via those classes.
class Class(base.KotatsuClass):
    """Create couchdb classes."""
    scope = {}
    def __new__(cls, name, bases, dct):
        # These are methods that end up on the class
        def obj__new__(cls, *args, **kwargs):
            """Construct an object."""
            print("Allocating couchdb document for object of type", cls.__name__)
            id = create_couch(None, 'object', cls.__name__)
            v = openorcreate(id, 'object')

            obj = object.__new__(cls, *args, **kwargs)
            obj._id = v['_id']
            obj._rev = v['_rev']
            return obj

        def obj__save__(self):
            """Save the object once it's been dereferenced."""
            print("Saving: ", self)
            # Save an object once we're done with it.
            v = c.openDoc('moo', self._id)
            if v['_rev'] != self._rev:
                raise Exception('revision mismatch', v['_rev'])
            doc = {'_id': self._id,
                   '_rev': v['_rev'],
                   'type': v['type'],
                   'value': {x: self.__dict__[x]
                             for x in self.__dict__
                             if (x not in skip_list)}}
            if isinstance(self, type):
                doc['parents'] = [x.__name__ for x in bases]
            else: 
                doc['class'] = self.__class__.__name__
            v = c.saveDoc('moo',
                          # Filter out internal names when saving
                          couch.jsonsave(doc),
                          self._id)

        def obj__delete__(self):
            """Delete the object from couchdb."""
            v = c.deleteDoc('moo', self._id, self._rev)
            print(v)

        print("Allocating or loading couchdb document for class", name, "of types", [x.__name__ for x in bases])
        v = openorcreate(name, 'class')
        attr = {'__new__':obj__new__,
                '__save__':obj__save__, 
                '__delete__':obj__delete__,
                '__scope__': {},
                '_id': name,
                '_rev': v['_rev']}

        if '__init__' in dct:
            print('INIT WOULD BE LOST', name)
            attr['__init__'] = dct['__init__']

        if  len(v['value']) == 0:
            # Create the object
            doc = {'_id': v['_id'],
                   '_rev': v['_rev'],
                   'type': v['type'],
                   'parents': [x.__name__ for x in bases],
                   'value': {x: dct[x]
                             for x in dct
                             if (x not in skip_list)}}
            new_v = c.saveDoc('moo',
                              couch.jsonsave(doc),
                              name)
            # New revision
            attr['_rev'] = new_v['rev']
            attr.update(dct)
            obj = type.__new__(cls, v['_id'], bases, attr)
        else:
            # Load the object

            # document references
            # FIXME: curry_load all leaf nodes, not just first level
            for key, value in v['value'].items():
                if type(value) is str and value.startswith("#moo://"):
                    id = value[7:]
                    prop = c.openDoc('moo', id)
                    if 'class' in prop:
                        attr[key] = property(curry_load(id, Class.scope, prop['class']))
                    else:
                        attr[key] = property(curry_load(id, Class.scope))
                else:
                    attr[key] = value

            obj = type.__new__(cls, v['_id'], bases, attr)

            # methods
            for name, value in attr.items():
                if type(value) is str:
                    if value.startswith('#python'):
                        start = 'def rebuild(self):'
                        end = '    return types.MethodType({0}, obj)'.format(name)
                        code = compile(start + value + end, 'couchdb', 'exec')
                        eglobal = {'types':types, 'obj':obj}
                        eglobal.update(Class.scope)
                        elocal = {}
                        exec(code, eglobal, elocal)
                        setattr(obj, name, elocal['rebuild'](obj))
        return obj

#    def __init__(cls, name, bases, dct):
#        super(Class, cls).__init__(name, bases, dct)

# Top of the tree
class Object(base.KotatsuObject, metaclass = Class):
    """Creates persistent couchdb stored objects.

    An object has dynamic methods associated with it,
    These are known as 'verbs'.
    An object has a parent object, and one or more verbs.
    A common (and thus given special syntax) verb is a property.
    """
    pass

def curry_load(id, scope, cls = None):
    """Delicious curry of life."""
    print("Curried:      ", cls, id)
    def curried_load():
        if cls:
            # Object
            loaded_cls = load(cls, scope)
            scope.update({cls:loaded_cls[cls]})
            return loaded_cls[cls](id)
        else:
            # Class
            return load(id, scope)
    return curried_load

def load(id, scope = {'Object':Object}):
    """Reconstruct the class tree needed to produce working objects.

    scope is a namespace dictionary.
    Returns the namespace dictionary needed to instantiate the object."""
    print("Loading", id)
    v = c.openDoc('moo', id)
    # Fallback in case scope is missing kotatsu entirely
    if 'Object' not in scope:
        scope['Object'] = Object
    if not missing(v):
        # Search for missing parents to build consistent children
        for each in v['parents']:
            if each not in scope:
                scope.update(load(each, scope))
        # Scope should be complete, load this
        if v['parents']:
            namespace = {'scope':scope, 'v':v}
            exec('class {name}(*[scope[x] for x in v["parents"]]): pass'.format(name=id), namespace)
            scope[id] = namespace[id]
        return scope
    raise Exception("Object not found.", id)
