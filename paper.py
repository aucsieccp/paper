class Delete(webapp2.RequestHandler):
	def get(self):
		key=data.key() //用key取得資料
		the data=db.get(key) //讀取key data
	
		data=Data(key_name='paper') //寫入paper
		data.put()
	
		the_data=db.get_by_key_name('paper') //刪除
		db.delete(the_data)//刪除資料庫
	
		query = Paper.all() //刪除多筆資料
		query.filter('name =','paper')
		papers = query.fetch(10,10) //刪除10筆資料
		db.delete(papers)