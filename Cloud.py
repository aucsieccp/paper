from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

MAIN_PAGE_HTML = """\
<html>
	<body>
		<form action="/AddPage" method="post">
			<div><input type="submit" value="Add"></div>
		</form>
  </body>
</html>

"""


AddPage_HTML = """\
<html>
	<body>
		<form action="/add" method="post">
		<div>Publish year:<br><input name="publish_year" rows="3" cols="60"></input></div>
		<div>Source:<br><input name="source" rows="3" cols="60"></input></div>
		<div>Title:<br><input name="title" rows="3" cols="60"></input></div>
		<div><input type="submit" value="add"></div>
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
	
class AddPage(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(AddPage_HTML)
	
class Add(webapp2.RequestHandler):
	def post(self):
		uuu = users.get_current_user()
		name = uuu.nickname()
		publish_year = self.request.get("publish_year")
		source = self.request.get("source")
		title = self.request.get("title")
		new_paper = Paper(name=name,publish_year=publish_year,title=title,source=source)
		new_paper_key = new_paper.put()
		
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('Sucess')

class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			qry = Paper.query()
			for a in qry:
				self.response.write("%s-%s-%s-%s-%s<br>" %(a.publish_year,a.source,a.title,a.name,a.time))
			self.response.headers['Content-Type'] = 'text/html'
			self.response.write('<a href="%s">Sign Out<a><br>' % users.create_logout_url(self.request.url))
		else:
			self.redirect(users.create_login_url(self.request.url))
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(MAIN_PAGE_HTML)

app = webapp2.WSGIApplication([
	('/',MainPage),
	('/AddPage',AddPage),
	('/add',Add),
], debug=True)
