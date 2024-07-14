import sys, os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql
import settings


#Connection me tin vasi me to settings.py
def connection():
    con = pymysql.connect(host=settings.mysql_host, port=settings.mysql_port, user=settings.mysql_user, passwd=settings.mysql_passwd, db=settings.mysql_schema)
    return con



def updateRank(rank1, rank2, movieTitle):
    con = connection()
    cur = con.cursor()

    try: #vathmologies se float 
        rank1 = float(rank1)
        rank2 = float(rank2)
    except ValueError:
        return [("status",), ("error",)]
    
    #elenxos an einai metaksi 0 kai 10 
    if not (0 <= rank1 <= 10 and 0 <= rank2 <= 10):
        return [("status",), ("error",)]

    average = (rank1 + rank2) / 2 #mesos oros ton 2 

    try: #search tin trexousa vathmologia ths tainias
        cur.execute("SELECT rank \
                    FROM movie \
                    WHERE title = %s", (movieTitle,))
        result = cur.fetchone() #save vathmologia 

        if result:
            current = result[0]
            
            #nea vathmologia, an den exei tote ...
            newrank = average if current is None else (current + average) / 2
            
            #update to rank
            cur.execute("UPDATE movie SET rank = %s WHERE title = %s", (newrank, movieTitle))
            con.commit()
            
            return [("status",), ("ok",)]
        else:
            return [("status",), ("error",)]
    except:
        return [("status",), ("error",)]
    
    finally:
        cur.close()
        con.close()

def colleaguesOfColleagues(actorId1, actorId2):
    con = connection()
    cur = con.cursor()

    #tainies pou exei paiksei o actor 1 
    cur.execute("SELECT movie_id \
                FROM role \
                WHERE actor_id = %s", (actorId1,))
    m_actors1 = cur.fetchall()

    #kenos xoros gia na mpoun oi synadelfoi 
    colleagues1 = set() 
    
    #synadelfoi tou actor1
    for movie in m_actors1:
        cur.execute("SELECT actor_id \
                    FROM role \
                    WHERE movie_id = %s \
                    AND actor_id != %s", (movie[0], actorId1)) 
        
        actors = cur.fetchall()
        for actor in actors:
            colleagues1.add(actor[0]) #prosthiki 

    # tainies tou actorId2
    cur.execute("SELECT movie_id \
                FROM role \
                WHERE actor_id = %s", (actorId2,))
    m_actor2 = cur.fetchall()

    #xoros gia tous synadelfous 
    colleagues2 = set() 

    #synadelfoi tou actor2
    for movie in m_actor2:
        cur.execute("SELECT actor_id \
                    FROM role \
                    WHERE movie_id = %s \
                    AND actor_id != %s", (movie[0], actorId2))
        
        actors = cur.fetchall()
        
        for actor in actors:
            colleagues2.add(actor[0])

    #tomh ton 2 synolwn gia na broume tous koinous synadcelfous 
    common = colleagues1 & colleagues2

    results = [] 


    #gia kathe enean mesa sto common colleagues 
    for colleague in common:
        #tainies pou exei paizei o kathe enas
        
        cur.execute("SELECT movie_id \
                    FROM role \
                    WHERE actor_id = %s", (colleague,))
        movies = cur.fetchall() #apothikeysh sto movies 
        
        #titlos ths tainias pou antistoixei me to trexon movieid 
        for movie in movies:
            cur.execute("SELECT title \
                        FROM movie \
                        WHERE movie_id = %s", (movie[0],))
            movie_title = cur.fetchone()[0] #apothikeysh 

            #prosthiki apotelesmatos sthn lisa
            results.append((movie_title, colleague, colleague, actorId1, actorId2))

    cur.close()
    con.close()

    return [("movieTitle", "colleagueOfActor1", "colleagueOfActor2", "actor1", "actor2",)] + results

def actorPairs(actorId):
    con = connection()
    cur = con.cursor()

    #eidi tainiwn gia ton actor 
    cur.execute("SELECT genre_id \
                FROM movie_has_genre \
                WHERE movie_id IN \
                    (SELECT movie_id \
                     FROM role \
                     WHERE actor_id = %s)", (actorId,))
    genres_actor = cur.fetchall() 
    
    #apothikeysh sto synolo 
    genres_actor = set([genre[0] for genre in genres_actor])

    #actors pou exoyn paiksei se tainies apo ayto to gerne
    actors = set()

    for genre in genres_actor:
        #tainies tou eidous 
        cur.execute("SELECT movie_id \
                    FROM movie_has_genre \
                    WHERE genre_id = %s", (genre,))
        movies = cur.fetchall() 
        
        movie_ids = [movie[0] for movie in movies]

        #gia thn kathe tainia tous actors pou exoun paiksei 
        for movie_id in movie_ids:
            cur.execute("SELECT actor_id \
                        FROM role \
                        WHERE movie_id = %s \
                        AND actor_id != %s", (movie_id, actorId))
            other_actors = cur.fetchall()

            #apothikeysh twn actors 
            for other_actor in other_actors:
                actors.add(other_actor[0])

    results = []

    #an kathe actor exei paiksei se toulaxiston 7 tainies
    for actor in actors:
        cur.execute("SELECT genre_id \
                    FROM movie_has_genre \
                    WHERE movie_id IN \
                        (SELECT movie_id \
                        FROM role \
                        WHERE actor_id = %s)", (actor,))
        genres_count = cur.fetchall()

        #set apo thn lista me ta eidi 
        #an h synthiki true tote add tpn actor sto result
        if len(set([genre[0] for genre in genres_count])) >= 7:
            results.append((actor,))

    cur.close()
    con.close()

    return [("actorId",)] + results

def selectTopNactors(n):
    con = connection()
    cur = con.cursor()

    # ola ta eidi twn tainiwn 
    cur.execute("SELECT genre_id, genre_name \
                FROM genre")
    genres = cur.fetchall()

    results = []

    #gia kathe eidos
    for genre in genres:
        genre_id = genre[0]
        genre_name = genre[1]

        #oles tis tainies poy exei to sygkekrimeno eidos 
        cur.execute("SELECT movie_id \
                    FROM movie_has_genre \
                    WHERE genre_id = %s", (genre_id,))
        movies = cur.fetchall()
        
        #add sthn lista
        movie_ids = [movie[0] for movie in movies]


        actorcount = {} #count movie actors 
        for movie_id in movie_ids:
            # actors pou exoyn paiksei sthn tainia 
            cur.execute("SELECT actor_id \
                        FROM role \
                        WHERE movie_id = %s", (movie_id,))
            actors = cur.fetchall()

            #lexiko poy krata ton arithmo tainiwn poy exei paikseo sto sygkekrimeno eidos.
            for actor in actors:
                if actor[0] in actorcount:
                    actorcount[actor[0]] += 1
                else:
                    actorcount[actor[0]] = 1

        # taksinomei thn lista twn tuples, 
        sort = sorted(actorcount.items(), key=lambda x: x[1], reverse=True) #x kathe tuple  x[1] arithmos tn tainiwn kai to reverse=True fthinousa h taksinomisi.  

        count = 0
        for actor in sort:
            #an to count einai oso to input 
            if count >= n:
                break
            #prosthiki sthn lista 
            results.append((genre_name, actor[0], actor[1]))
            count += 1

    cur.close()
    con.close()

    return [("genreName", "actorId", "numberOfMovies",)] + results


def traceActorInfluence(actorId):
    con = connection()
    cur = con.cursor()

    influenced_actors = set()
    #set poy exei arxika ton actorid, gia tous actors poy prepei na elenxthoun    
    actors_to_check = {actorId}

    #oso yparxoyn actors sto actor to check
    while actors_to_check:
        current_actor = actors_to_check.pop() #pop ton actor gia check 

        # oles oi tainies toucurrent_actor
        cur.execute("SELECT movie_id \
                    FROM role \
                    WHERE actor_id = %s", (current_actor,))
        movies = cur.fetchall()

        #gia kathe tainia tou actor
        for movie in movies:
            movie_id = movie[0]

           #vriskoyme to etos kai to eidos 
            cur.execute("SELECT year \
                        FROM movie \
                        WHERE movie_id = %s", (movie_id,))
            year = cur.fetchone()[0]
            cur.execute("SELECT genre_id \
                        FROM movie_has_genre \
                        WHERE movie_id = %s", (movie_id,))
            genres = cur.fetchall()
            
            #gia kathe eidos 
            for genre in genres:
                genre_id = genre[0]

                # tainies tou eidoys poy eginan meta to year 
                cur.execute("SELECT movie_id FROM movie WHERE year > %s \
                             AND movie_id IN \
                                (SELECT movie_id \
                                 FROM movie_has_genre \
                                 WHERE genre_id = %s)", (year, genre_id))
                later_movies = cur.fetchall()

                #gia kathe metagenesteri tainia 
                for later_movie in later_movies:
                    later_movie_id = later_movie[0]

                    # to movie id ths kai toys actors poy exoyn paiksei
                    cur.execute("SELECT actor_id \
                                FROM role \
                                WHERE movie_id = %s", (later_movie_id,))
                    
                    influenced_actors_results = cur.fetchall()

                    #gia kathe actor, check an einai sto influenced actors, an den einai ton vazei kai sto actors to check gia elegxo.
                    for influenced_actor in influenced_actors_results:
                        if influenced_actor[0] not in influenced_actors:
                            influenced_actors.add(influenced_actor[0])
                            actors_to_check.add(influenced_actor[0])

    cur.close()
    con.close()

    return [("influencedActorId",)] + [(actor,) for actor in influenced_actors]
