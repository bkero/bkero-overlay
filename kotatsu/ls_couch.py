#!/usr/bin/env python3.0
import config
import couch

couch.debug = True

c = couch.Couch(config.couchdb_host)
for each in c.listDb():
    print('Database: ', each)
    c.infoDb(each)
    
    c.listDoc(each)
