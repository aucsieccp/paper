from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
import webapp2
import sys
import datetime
import database

reload(sys)
sys.setdefaultencoding('utf-8')

Upload_HTML = """\
<html>
	<body>
		<form action="%s" method="post" enctype="multipart/form-data">
		<div>Uplaod Paper Title <input name="resource" value="%s"></input><div>
		Upload File: 	<input type="file" name="file"><br>
						<input type="submit" name="file_name" value="Upload!!">
		</form>
	</body>
</html>

"""

class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.response.headers['Content-Type'] = 'text/html'
			qry = database.Paper.query()
			self.response.write('<form method="post"><TABLE BORDER="1">')
			self.response.write('	<TR><TD>Year</TD> \
										<TD>Source</TD><TD>title</TD><TD>Time</TD><TD>Paper</TD><TD>ppt</TD><TD>Edit</TD><TD>Delete</TD>	\
									</TR>')
			for a in qry:
				self.response.write('<TR>')
				self.response.write('<TD>%s</TD>' % a.publish_year)
				self.response.write('<TD>%s</TD>' % a.source)
				self.response.write('<TD>%s</TD>' % a.title)
				self.response.write('<TD>%s</TD>' % a.time)
				if a.file_key == None:
					self.response.write('<TD>')
					self.response.write('<button name="resource" value="%s" formaction="/Upload_page" type="submit">Upload_Paper</button>' % a.title)
					self.response.write('</TD>')
				else:
					self.response.write('<TD>')
					self.response.write('<button name="resource" value="%s" formaction="/File/DownLoad" type="submit">DownLoad</button>' % a.file_key)
					self.response.write('</TD>')
				if a.file_ppt == None:
					self.response.write('<TD>')
					self.response.write('<button name="resource" value="%s" formaction="/Upload_ppt_page" type="submit">Upload_ppt</button>' % a.title)
					self.response.write('</TD>')
				else:
					self.response.write('<TD>')
					self.response.write('<button name="resource" value="%s" formaction="/File/DownLoad" type="submit">DownLoad</button>' % a.file_ppt)
					self.response.write('</TD>')
				self.response.write('<TD>')
				self.response.write('<button name="resource" value="%s" formaction="/edit/edit_page" type="submit">Edit</button>' % a.key.id())
				self.response.write('</TD>')
				self.response.write('<TD>')
				self.response.write('<button name="id" value="%s" formaction="/File/Delete" type="submit">Delete</button>' % a.key.id())
				self.response.write('</TD>')
				self.response.write('</TR>')
			self.response.write('</TABLE>')
			self.response.write('<br><button name="name" value="None" formaction="/Add/AddPage" type"submit">Add</button>')
			self.response.write('<br><button name="clean" value="clean" formaction="/clean_page" type="submit">Clean</button>')
			self.response.write('</form>')
			self.response.write('<br><a href="%s">Logout</a>' % users.create_logout_url(self.request.url))
		else:
			self.redirect(users.create_login_url(self.request.url))
		
class Clean_Data(webapp2.RequestHandler):
	def post(self):
		ndb.delete_multi(
		database.Paper.query().fetch(keys_only=True)
		)
		
		qry = blobstore.BlobInfo.all()
		for blobinfo in qry:
			blobinfo.delete()
			
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('Clean sucess<br>')
		self.response.write('<a href="%s">Main Page</a>' %('/'))

class  Upload_page(webapp2.RequestHandler):
	def post(self):
		title = self.request.get('resource')
		upload_url = blobstore.create_upload_url('/File/upload')
		self.response.write(Upload_HTML % (upload_url,title))
		self.response.headers['Content-Type'] = 'text/html'
		
class Upload_ppt_page(webapp2.RequestHandler):
	def post(self):
		title = self.request.get('resource')
		upload_url = blobstore.create_upload_url('/File/upload_ppt')
		self.response.write(Upload_HTML % (upload_url,title))
		self.response.headers['Content-Type'] = 'text/html'
	
app = webapp2.WSGIApplication([
	('/',MainPage),
	('/clean_page',Clean_Data),
	('/Upload_page',Upload_page),
	('/Upload_ppt_page',Upload_ppt_page),
], debug=True)
