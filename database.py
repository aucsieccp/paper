from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
import sys
import datetime

class Paper(ndb.Model):
	title = ndb.StringProperty()
	source = ndb.StringProperty()
	name = ndb.StringProperty()
	time = ndb.DateTimeProperty(auto_now_add=True)
	publish_year = ndb.StringProperty()
	file_key = ndb.StringProperty()
