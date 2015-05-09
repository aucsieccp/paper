import webapp2
import datetime
import database
from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		try:
			upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
			blob_info = upload_files[0]
			self.response.headers['Content-Type'] = 'text/html'
			pp = str(blob_info.key())
			title = self.request.get('resource')

			q = database.Paper.query(database.Paper.title == title).fetch()
			for g in q:
				g.file_key = pp
				g.put()

			self.response.write('<h1>Upload Done~~!!!</h1>')
			self.response.write('<a href="%s">Main Page</a>' %('/'))
		except:
			self.redirect('/')
		
class Upload_ppt_Handler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		try:
			upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
			blob_info = upload_files[0]
			self.response.headers['Content-Type'] = 'text/html'
			pp = str(blob_info.key())
			title = self.request.get('resource')

			q = database.Paper.query(database.Paper.title == title).fetch()
			for g in q:
				g.file_ppt = pp
				g.put()
			self.response.write('<h1>PPT Upload Done~~!!!</h1>')
			self.response.write('<a href="%s">Main Page</a>' %('/'))
		except:
			self.redirect('/')

class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def post(self):
		resource = self.request.get('resource')
		blob_info = blobstore.BlobInfo.get(resource)
		self.send_blob(blob_info)
		self.response.headers['Content-Type'] = 'text/html'

class DeleteHandler(webapp2.RequestHandler):
	def post(self):

		
		self.response.write('Delete Sucess')
		self.response.headers['Content-Type'] = 'text/html'
		
app = webapp2.WSGIApplication([
	('/File/upload', UploadHandler),
	('/File/DownLoad',DownloadHandler),
	('/File/upload_ppt',Upload_ppt_Handler),
	('/File/Delete',DeleteHandler),
], debug=True)