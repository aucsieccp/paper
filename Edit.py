import webapp2
import datetime
from google.appengine.api import users
from google.appengine.ext import ndb


EDIT_PAGE_HTML = """\
<html>
	<body>
	<form action="/edit" method="post">
		<div>Publish Year:<textarea name="publish_year" rows="1" cols="60"></textarea></div>
		<div>Source:<textarea name="source" rows="1" cols="60"></textarea></div>
		<div>Title:<textarea name="title" rows="1" cols="60"></textarea></div>
		<div><input type="submit" value="update"></div>
		<div><input type="button" value="back"; reutrn false;></div>
	</form>
	</body>
</html>
"""

class Data(ndb.Model):
	publish_year = ndb.StringProperty()
	source = ndb.StringProperty()
	title = ndb.StringProperty()
	lastupdate = ndb.StringProperty()
	user = ndb.StringProperty()

class Edit(webapp2.RequestHandler):
	def get(self):
		people = users.get_current_user()
		current = datetime.datetime.now()

		if people == user.query():
			publish_year = self.request.get("publish_year")
			source = self.request.get("source")
			title = self.request.get("title")
			lastupdate = self.request.get(current)
			user = self.request.get(user)
			newupdate = Data(publish_year=publish_year,
				source=source,
				title=title,
				lastupdate=lastupdate,
				)
			self.response.write(people)
		else :
			return

class show(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(EDIT_PAGE_HTML)

app = webapp2.WSGIApplication([
	('/', show),
	('/edit', Edit),
], debug=True)
