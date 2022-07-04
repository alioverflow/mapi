import requests
import mysql.connector
def mysqloperations():
    try:
        connection = mysql.connector.connect(host='localhost',
                database='mapidb',
                user='mapi',
                password='mapi')

        url='https://api.themoviedb.org/3/discover/movie?api_key=6ad473f9a4be91546b3049c7a2654697&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_watch_monetization_types=flatrate&page='
        if connection.is_connected():
            cur = connection.cursor()
            PAGE=500
            for i in range(1,PAGE):
                r = requests.get(url+str(i))
                data = r.json()
                for y in range(len(data["results"])):
                    films = data["results"][y]
                    filmscheck = (films["id"],)
                    SQLcheck = "SELECT movie_id FROM movies WHERE movie_id=%s"
                    cur.execute(SQLcheck,filmscheck)
                    res = cur.fetchall()
                    if len(res)!=0:
              
                        continue;
                    else:
                        sql = "INSERT INTO movies (movie_id, movie_title, vote_average, movie_overview) VALUES (%s, %s, %s, %s)"
                        val=(films["id"],films["title"],films["vote_average"],films["overview"])
                        cur.execute(sql,val)
                        connection.commit()
    except Error as e:
        print("MySQL Connection Error")

    finally:
        if connection.is_connected():
            cur.close()
            connection.close()
            print("MySQL has been closed")
