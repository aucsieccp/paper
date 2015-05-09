import webapp2
import datetime
import database
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

EDIT_PAGE_HTML = """\
<html>
	<body>
	<form action="/edit/edit" method="post">
		<div>Publish year:<br><input name="publish_year" value="%s" rows="3" cols="60"></input></div>
		<div>Source:<br><input name="source" value="%s" rows="3" cols="60"></input></div>
		<div>Title:<br><input name="title" value="%s" rows="3" cols="60"></input></div>
		<div><input type="hidden" name="id" value="%s"></div>
		<div><input type="submit" value="edit"></div>
	</form>
	</body>
</html>
"""

class edit(blobstore_handlers.BlobstoreDownloadHandler):
	def post(self):
		id = self.request.get('id')
		q = database.Paper.get_by_id(id)
		q.publish_year = self.request.get('publish_year')
		q.source = self.request.get('source')
		q.title = self.request.get('title')
		q.put()
		self.response.write('Edit Sucess')
		self.response.write('<br><a href="%s">Main Page</a>' %('/'))
		self.response.headers['Content-Type'] = 'text/html'
	

class show(webapp2.RequestHandler):
	def post(self):
		r_id = self.request.get('resource')
		#q = database.Paper.query(database.Paper.title == r_title)
		q = database.Paper.get_by_id(r_id)
		
		self.response.write(EDIT_PAGE_HTML % (q.publish_year,q.source,q.title,r_id))
		self.response.headers['Content-Type'] = 'text/html'

app = webapp2.WSGIApplication([
	('/edit/edit_page',show),
	('/edit/edit',edit),
], debug=True)
