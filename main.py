import webapp2
import MySQLdb
import gauthen
import cgi

class MainPage(webapp2.RequestHandler):
 def get(self):
  self.response.headers["Content-Type"] = "text/html"
  self.response.write("Hello World")

#class SQLtest(webapp2.RequestHandler):
# def get(self):
#  self.response.headers["Content-Type"] = "text/html"
#  conn = MySQLdb.connect(unix_socket = "/home/ec2-user/cloudsql/central-apex-259103:us-central1:jtroyergae", user = gauthen.SQL_USER, passwd = gauthen.SQL_PASSWD, db = "labgmain")
#  cursor = conn.cursor()
#  cursor.execute("SELCT * FROM test;")
#  results = cursor.fetchall()
#  for rec in results:
#   self.response.write(rec)

class frontpage(webapp2.RequestHandler):
 def get(self):
  self.response.headers["Content-Type"] = "text/html"
  user = ""
  sessionid = 0
  #First checkf or session.
  if self.request.cookies.get("sessioncookie") == "None":
   #If there is none, create a cookie
   sessionid = "%032x" % random.getrandbits(128)
   conn = MySQLdb.connect(unix_socket = gauthen.SQL_SOCKET, user = gauthen.SQL_USER, passwd = gauthen.SQL_PASSWD, db = "labgmain")
   cursor = conn.cursor()
   cursor.execute("INSERT INTO sessions(sessid) VALUES \"" + sessionid + "\";")
   cursor.close()
   conn.commit()
   conn.closer()
   self.response.set_cookie("sessioncookie", sessionid, max_age=1800)
  else:
   #If there is get it
   sessionid = self.request.cookies.get("sessioncookie")
   conn = MySQLdb.connect(host = gauthen.SQL_HOST, user = gauthen.SQL_USER, passwd = gauthen.SQL_PASSWD, db = "labgmain")
   cursor = conn.cursor()
   cursor.execute("SELECT username FROM sessions WHERE sessid=\"" + sessionid + "\";")
   results = cursor.fetchall()
   user = results[0][0]
   cursor.close()
   conn.close()
  #Now get the user. If there is none ask them to create one
  if user == "NULL" or user == "":
   self.response.write("""
<html>
<head>
<title>New User</title>
</head>
<body>
<form action="/landing" method="get">
 <input type=text name=user value="username here">
 <input type=hidden name=id value=""")
   self.response.write(sessionid)
   self.response.write(""">
 <input type=submit>
</form>
</body>
</html>
""")
  else:
   #If we have a user then show them the plain old button presses page
   self.response.write("""
<html>
<head>
<title>returning user</title>
</head>
<body>
You've pressed the button
""")

   conn = MySQLdb.connect(unix_socket = gauthen.SQL_SOCKET, user = gauthen.SQL_USER, passwd = gauthen.SQL_PASSWD, db = "labgmain")
   cursor = conn.cursor()
   cursor.execute("SELECT number FROM presses WHERE user=\"" + user + "\";")
   results = cursor.fetchall()
   self.response.write(results[0][0])
   self.response.write("""
times.<b>
<form action="/pressed" method="get">
<input type=hidden name=user value=\"""")
   self.response.write(user)
   self.response.write("""
<input type=submit>
</form>
</body>
</html>""")


#For creating a new user
class landingpad(webapp2.RequestHanlder):
 def get(self):
  form = cgi.FieldStorage()
  conn = MySQLdb.connect(unix_socket = gauthen.SQL_SOCKET, user = gauthen.SQL_USER, passwd = gauthen.SQL_PASSWD, db = "labgmain")
  cursor = conn.cursor()
  form = cgi.FieldStorage()
  cursor.execute("UPDATE sessions SET username=\"" + form["user"] + "\" WHERE sessid=" + form["id"] + ";")
  cursor.close()
  conn.commit()
  cursor = conn.cursor()
  cursor.execute("INSERT INTO presses(user, number) VALUES (\"" + form["user"] +"\", 0);")
  cursor.close()
  conn.commit()
  #now redirect back to the main page
  self.redirect("https://central-apex-259103.appspot.com/")

class pressHandler(webapp2.RequestHandler):
 def get(self):
  conn = MySQLdb.connect(unix_socket = gauthen.SQL_SOCKET, user = gauthen.SQL_USER, passwd = gauthen.SQL_PASSWD, db = "labgmain")
  cursor = conn.cursor()
  form = cgi.FieldStorage()
  cursor.execute("UPDATE presses SET number = number+1 WHERE user = \"" + form["user"] + "\";")
  cursor.close()
  conn.commit()
  self.redirect("https://central-apex-259103.appspot.com/")

app = webapp2.WSGIApplication([("/", frontpage), ("/landing", landingpad), ("/pressed", pressHandler)], debug=True)

