from flask import Flask	
import requests
import mysql.connector
import json
app = Flask(__name__)

@app.route('/<string:apikey>/api/v1/filmdatas/<int:count>/<int:page>', methods=['GET'])
def getfilmdata(apikey,count,page):
    view_list=[]
    mydb = mysql.connector.connect(
    		host="localhost",
    		user="mapi",
    		password="mapi",
    		database="mapidb")
    curcheck = mydb.cursor()
    checkapikey ="SELECT * FROM users WHERE user_key = %s"
    userkey=(apikey,)
    curcheck=mydb.cursor()
    curcheck.execute(checkapikey,userkey)
    checkresults = curcheck.fetchall()
    curcheck.close()
    if len(checkresults)>0:
        cur = mydb.cursor()
        cur.execute("SELECT * FROM movies")
        results = cur.fetchall()
        results = results[0+(count*page):count*(page+1)]
        for x in results:
        	view_list.append(x)
        jsonresult = json.dumps(view_list)
        print(type(jsonresult))
        cur.close()
        mydb.close()
        return jsonresult
    else:
        return "apikey invalid"

@app.route('/api/v1/useracts/<string:userid>/<string:movieid>/<string:voteuser>/<string:moviereview>', methods=['POST'])
def postUserAct(userid,movieid,voteuser,moviereview):
	if "." not in voteuser and "," not in voteuser:
		try:
			voteuser_int = int(voteuser)
			if voteuser_int>0 and voteuser_int<10:
				mydb = mysql.connector.connect(
					host="localhost",
					user="mapi",
					password="mapi",
					database="mapidb")
				cur = mydb.cursor()
				sql="INSERT INTO useracts(user_id,movie_id,vote_user,movie_review) VALUES (%s, %s, %s, %s)"
				val = (userid,movieid,voteuser,moviereview)
				cur.execute(sql,val)
				mydb.commit()
				cur.close()
				mydb.close()
				return "OK"
			else:
				return "vote must be 0<vote<10"
		except:
			return "voteuser must be integer"
	else:
		return "please check your vote for film: vote must be integer"

@app.route('/api/v1/userdata/<string:userid>/<string:movieid>/', methods=['GET'])
def userdata(userid,movieid):
	filmsdetailslist=[]
	mydb = mysql.connector.connect(
		host="localhost",
		user="mapi",
		password="mapi",
		database="mapidb")
	cur=mydb.cursor()
	sql = "SELECT useracts.user_id,useracts.movie_id,movies.movie_title,useracts.vote_user,useracts.movie_review,movies.movie_overview,movies.vote_average FROM useracts INNER JOIN movies ON useracts.movie_id=movies.movie_id WHERE useracts.movie_id =%s AND useracts.user_id =%s"
	moviesids = (movieid,userid,)
	cur.execute(sql,moviesids)
	res = cur.fetchall()
	jsonresult = json.dumps(res)
	cur.close()
	mydb.close()
	return jsonresult

app.run()
