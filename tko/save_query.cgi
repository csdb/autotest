#!/usr/bin/python

import os, cgi, cgitb, time, urllib
import db, unique_cookie

## setting script globals
form = cgi.FieldStorage()
if 'label' in form.keys():
	comment = form['label'].value
else:
	comment = ''
dict_url = {}
for key in form.keys():
	dict_url[key] = form[key].value

tm = time.asctime()
uid = unique_cookie.unique_id('tko_history')
HTTP_REFERER = os.environ.get('HTTP_REFERER')
if HTTP_REFERER == None:
	## fall back strategy for proxy connection
	## substitute relative url
	HTTP_REFERER = 'compose_query.cgi?' + urllib.urlencode(dict_url)	


class QueryHistoryError(Exception):
	pass


def log_query():
	db_obj = db.db()
	data_to_insert = {'uid':uid, 'time_created':tm,
			  'user_comment':comment, 'url':HTTP_REFERER }
	try:
		db_obj.insert('query_history', data_to_insert)
	except:
		raise QueryHistoryError("Could not save query")


def body():
	log_query()
	print '<b>%s</b><br><br>' % "Your query has been saved"
	print 'time: %s<br>' % tm
	print 'comments: %s<br><br>' % comment
	print '<table><tr align="center">'
	print '<td align="center">'
	print '<a href="query_history.cgi">View saved queries</a>&nbsp;&nbsp;'
	print '</td>'
	print '<td align="center">'
	print '<a href="%s">Back to Autotest</a><br>' % HTTP_REFERER
	print '</td>'


def main():
	print "Content-type: text/html\n"
	print '<html><head><title>'
	print '</title></head>'
	print '<body>'
	body()
	print '</body>'
	print '</html>'


main()



