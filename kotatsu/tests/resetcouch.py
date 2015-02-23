#!/usr/bin/python3.0
import sys
sys.path[0] = ''

import config
import couch

couch.debug = True
# Clear the database before anything else is done.
c = couch.Couch(config.couchdb_host)
c.deleteDb('moo')
c.createDb('moo')
c.close()
