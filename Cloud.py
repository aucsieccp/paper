from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
import webapp2
import sys
import datetime
import database

reload(sys)
sys.setdefaultencoding('utf-8')


class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			qry = database.Paper.query()
			for a in qry:
				self.response.write("%s-%s-%s-%s-%s-%s<br>" %(a.publish_year,a.source,a.title,a.name,a.time,a.file_key))
			self.response.headers['Content-Type'] = 'text/html'
			self.response.write('<a href="%s">Sign Out<a><br>' % users.create_logout_url(self.request.url))
			self.response.headers['Content-Type'] = 'text/html'
			self.response.write('	<form method="post"> \
										<button formaction="/Add/AddPage" type="submit">add</button> \
									</form>')
			self.response.write('<a href="%s">Logout</a>' % users.create_logout_url(self.request.url))
		else:
			self.redirect(users.create_login_url(self.request.url))

		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('<br><button name="clean" value="clean" form action="/clean_page" type="submit">Clean</button>')
		self.response.write('<h1>Your myS3 file list</h1>')
		self.response.write('<form method="post"><TABLE BORDER="1">')
		self.response.write('<TR><TD>Year</TD><TD>Source</TD><TD>Name</TD><TD>Time</TD><<TD>publis</TD></TR>')

		qry = blobstore.BlobInfo.all()
		for blobinfo in qry:
			self.response.write('<TR>')	
			self.response.write('<TD>%s</TD>' % blobinfo.filename)
			self.response.write('<TD>%s</TD>' % str(blobinfo.creation))
			self.response.write('<TD>')
			#self.response.write('<button name="resource" value="%s" formaction="/myS3/download" type="submit">Download</button>' % str(blobinfo.key()))
			#self.response.write('<button name="resource" value="%s" formaction="/myS3/delete" type="submit">Delete</button>' % str(blobinfo.key()))
			self.response.write('</TD>')
			self.response.write('</TR>')
		
		self.response.write('</TABLE></form>')
		
class Clean_Data(webapp2.RequestHandler):
	def get(self):
		ndb.delete_multi(
		database.Paper.query().fetch(keys_only=True)
		)
		
		qry = blobstore.BlobInfo.all()
		for blobinfo in qry:
			blobinfo.delete()
			
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('Clean sucess<br>')
		self.response.write('<a href="%s">Main Page</a>' %('/'))


app = webapp2.WSGIApplication([
	('/',MainPage),
	('/clean_page',Clean_Data),
], debug=True)
