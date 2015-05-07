import webapp2
import datetime
import database
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
		blob_info = upload_files[0]
		self.response.headers['Content-Type'] = 'text/html'
		pp = str(blob_info.key())
		key = self.request.get('resource')
		
		self.response.write('<h1>%s!</h1>' % key)
		#test = database.Paper.get(title == file_name)
		#test = database.Paper.query(database.Paper.title == file_name).fetch()
		gg = database.Paper(id=key)
		gg.file_key = pp;
		gg.put()
		#new_paper = database.Paper(file_key=pp)
		#new_paper_key = new_paper.put()
		
		self.response.write('<h1>Upload Done~~!!!</h1>')
		self.response.write('<a href="%s">Main Page</a>' %('/'))

app = webapp2.WSGIApplication([
	('/upload/upload', UploadHandler),
], debug=True)