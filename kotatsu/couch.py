#!/usr/bin/env python
"""CouchDB interface."""
import http.client
import json
import inspect
import types
import base

debug = False

class KotatsuEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, types.FunctionType) or isinstance(obj, types.MethodType):
            source = inspect.getsource(obj)
            return '#python\n' + source
        elif isinstance(obj, base.KotatsuObject) or isinstance(obj, base.KotatsuClass):
            return '#moo://' + obj._id
        else:
            return json.JSONEncoder.default(self, obj)

def jsonload(httpr):
    return json.loads(httpr.read().decode('utf-8'))

def jsonsave(struct):
    return json.dumps(struct, cls=KotatsuEncoder)

def prettyPrint(r):
    import sys, inspect
    # This is the name of the function calling prettyPrint
    print(inspect.getframeinfo(sys._getframe(1), context=0)[2], json.dumps(r, sort_keys=True, indent=4))

class Couch:
    """Basic wrapper class for operations on a couchDB"""
    def __init__(self, host, port=5984, options=None):
        self.host = host
        self.port = port
        self.c = http.client.HTTPConnection(self.host, self.port)

    def close(self):
        self.c.close()

    # Database operations
    def createDb(self, dbName):
        """Creates a new database on the server"""

        httpr = self.put(''.join(['/',dbName,'/']), "")
        r = jsonload(httpr)
        if debug: prettyPrint(r)
        return r

    def deleteDb(self, dbName):
        """Deletes the database on the server"""
        httpr = self.delete(''.join(['/',dbName,'/']))
        r = jsonload(httpr)
        if debug: prettyPrint(r)
        return r

    def listDb(self):
        """List the databases on the server"""
        httpr = self.get('/_all_dbs')
        r = jsonload(httpr)
        if debug: prettyPrint(r)
        return r
        
    def infoDb(self, dbName):
        """Returns info about the couchDB"""
        httpr = self.get(''.join(['/', dbName, '/']))
        r = jsonload(httpr)
        if debug: prettyPrint(r)
        return r

    # Document operations
    def listDoc(self, dbName):
        """List all documents in a given database"""
        httpr = self.get(''.join(['/', dbName, '/', '_all_docs']))
        r = jsonload(httpr)
        if debug: prettyPrint(r)
        return r

    def openDoc(self, dbName, docId):
        """Open a document in a given database"""
        httpr = self.get(''.join(['/', dbName, '/', docId,]))
        r = jsonload(httpr)
        if debug: prettyPrint(r)
        return r

    def saveDoc(self, dbName, body, docId=None):
        """Save/create a document to/in a given database"""
        if docId:
            httpr = self.put(''.join(['/', dbName, '/', docId]), body)
        else:
            httpr = self.post(''.join(['/', dbName, '/']), body)
        r = jsonload(httpr)
        if debug: prettyPrint(r)
        return r

    def deleteDoc(self, dbName, docId, revId):
        r = self.delete(''.join(['/', dbName, '/', docId, '?rev=', revId], ))
        if debug: prettyPrint(r)
        return r

    # Basic http methods
    def get(self, uri):
        headers = {"Accept": "application/json"}
        self.c.request("GET", uri, None, headers)
        return self.c.getresponse()

    def post(self, uri, body):
        headers = {"Content-type": "application/json"}
        self.c.request('POST', uri, body, headers)
        return self.c.getresponse()

    def put(self, uri, body):
        if len(body) > 0:
            headers = {"Content-type": "application/json"}
            self.c.request("PUT", uri, body, headers)
        else:
            self.c.request("PUT", uri, body)
        return self.c.getresponse()

    def delete(self, uri):
        self.c.request("DELETE", uri)
        return self.c.getresponse()

