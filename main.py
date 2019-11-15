import webapp2
import MySQLdb
import gauthen
import cgi

class MainPage(webapp2.RequestHandler):
 def get(self):
  self.response.headers["Content-Type"] = "text/html"
  self.response.write("Hello World")

class frontpage(webapp2.RequestHandler):
 def get(self):
  self.response.headers["Content-Type"] = "text/html"
  user = ""
  sessionid = 0
  if self.request.cookies.get("sessioncookie") == "None":
   sessionid = "%032x" % random.getrandbits(128)
   conn = MySQLdb.connect(host = gauthen.SQL_HOST, user = gauthen.SQL_USER, passwd = gauthen.SQL_PASSWD, db = "labgmain")
   cursor = conn.cursor()
   cursor.execute("INSERT INTO sessions(sessid) VALUES \"" + sessionid + "\";")
   cursor.close()
   conn.commit()
   conn.closer()
   self.response.set_cookie("sessioncookie", sessionid, max_age=1800)
  else:
   sessionid = self.request.cookies.get("sessioncookie")
   conn = MySQLdb.connect(host = gauthen.SQL_HOST, user = gauthen.SQL_USER, passwd = gauthen.SQL_PASSWD, db = "labgmain")
   cursor = conn.cursor()
   cursor.execute("SELECT username FROM sessions WHERE sessid=\"" + sessionid + "\";")
   results = cursor.fetchall()
   user = results[0][0]
   cursor.close()
   conn.close()

  if user == "NULL" or user == "":
   self.response.write("""
<html>
<head>
<title>New User</title>
</head>
<body>
<form action="/landing" method="get">
 <input type=text name=user value="username here">
 <input type=hidden name=id value="""
self.response.write(sessionid)
self.response.write(""">
 <input type=submit>
</form>
</body>
</html>
""")
  else:
   self.response.write("""
<html>
<head>
<title>returning user</title>
</head>
<body>
You've pressed the button
""")

   conn = MySQLdb.connect(host = gauthen.SQL_HOST, user = gauthen.SQL_USER, passwd = gauthen.SQL_PASSWD, db = "labgmain")
   cursor = conn.cursor()
   cursor.excecute("SELECT number FROM presses WHERE user='" + user + "';")
   results = cursor.fetchall()
   self.response.write(results[0][0])
   self.response.write("""
times.<b>
<form action="/pressed" method="get">
<input type=submit>""")

class landingpad(webapp2.RequestHanlder):
 def get(self):
  form = cgi.FieldStorage()
  conn = MySQLdb.connect(host = gauthen.SQL_HOST, user = gauthen.SQL_USER, passwd = gauthen.SQL_PASSWD, db = "labgmain")
  cursor = conn.cursor()
  cursor.excecute("INSERT ")

app = webapp2.WSGIApplication([("/", frontpage), ("/old", MainPage)], debug=True)

