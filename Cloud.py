from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
import webapp2
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')
UPLOAD_HTML = """\
<html>
  <body>
    <form action="%s" method="post" enctype="multipart/form-data">
    </form>
  </body>
</html>
"""

class Paper(ndb.Model):
	title = ndb.StringProperty()
	source = ndb.StringProperty()
	name = ndb.StringProperty()
	time = ndb.DateTimeProperty(auto_now_add=True)
	publish_year = ndb.StringProperty()

class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			qry = Paper.query()
			for a in qry:
				self.response.write("%s-%s-%s-%s-%s<br>" %(a.publish_year,a.source,a.title,a.name,a.time))
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
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('<form method="post"><TABLE BORDER="1">')
		self.response.write('<TR><TD>Year</TD><TD>Source</TD><TD>Name</TD><TD>Time</TD><<TD>publis</TD></TR>')

		qry = Paper.query()
		for database in qry:
			self.response.write('<TR>')	
			self.response.write('<TD>%s</TD>' % database.publish_year)
			self.response.write('<TD>%s</TD>' % database.source)
			self.response.write('<TD>%s</TD>' % database.name)
			self.response.write('<TD>%s</TD>' % database.time)
			self.response.write('<TD>%s</TD>' % database.title)
			
			self.response.write('<TD>')
			self.response.write('<button name="resource" value="%s" formaction="/edit/edit" type="submit">edit</button>' %database.name)
			#self.response.write('<button name="resource" value="%s" formaction="/myS3/delete" type="submit">Delete</button>' % str(blobinfo.key()))
			self.response.write('</TD>')
			self.response.write('</TR>')
		
		self.response.write('</TABLE></form>')
		self.response.write('<a href="%s">Main Page</a>' %('/'))


app = webapp2.WSGIApplication([
	('/',MainPage),
], debug=True)
