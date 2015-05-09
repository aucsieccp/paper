from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
import sys
import datetime
import database

class File_list(webapp2.RequestHandler):
	def post(self):
		title = self.request.get('resource')
		q = database.Paper.query(database.Paper.title == title)
		for p in q:
			if p.file_key == None:
				self.response.write('GG')
			else:
				self.response.write('%s' % p.file_key)
		self.response.headers['Content-Type'] = 'text/html'

	
	
app = webapp2.WSGIApplication([
	('/file_list/file_list',File_list),
], debug=True)