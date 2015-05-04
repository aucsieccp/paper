import webapp2
import datetime
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
		blob_info = upload_files[0]
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('<h1>Upload Done~~!!!</h1>')
		self.response.write('<a href="%s">Main Page</a>' %('/'))




app = webapp2.WSGIApplication([
	('/upload/upload', UploadHandler),
], debug=True)