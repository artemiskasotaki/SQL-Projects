
#1
SELECT distinct m.title 
FROM movie m, role r, actor a, movie_has_genre mg, genre g
WHERE m.movie_id = r.movie_id
AND r.actor_id = a.actor_id #connects to role me to actor me vasi to actor_id
AND m.movie_id = mg.movie_id #antistoixa kai ta ypoloipa
AND mg.genre_id = g.genre_id
AND a.last_name = 'Allen'
AND g.genre_name = 'Comedy'; #to last name tou na einai allen kai na einai to eidos comedy

#2
SELECT DISTINCT director.last_name, movie.title AS title
FROM director, movie, movie_has_director, role, actor, movie_has_genre
WHERE director.director_id = movie_has_director.director_id
AND movie.movie_id = movie_has_director.movie_id  #connections twn pinakwn me vasi ta movie_id 
AND movie.movie_id = role.movie_id
AND role.actor_id = actor.actor_id
AND movie.movie_id = movie_has_genre.movie_id
AND actor.last_name = 'Allen'
AND director.director_id IN (
    SELECT d.director_id
    FROM director d, movie m, movie_has_genre mg, movie_has_director md
    WHERE d.director_id = md.director_id
    AND m.movie_id = md.movie_id
    AND m.movie_id = mg.movie_id
    GROUP BY d.director_id #omadopoihsh kata director_id
    HAVING COUNT(DISTINCT mg.genre_id) >= 2); #only directors poy exoyn skinothetisei 2 eidh tainiwn. 

#3
SELECT DISTINCT a.last_name
FROM actor a, role r, movie m, movie_has_director md, director d
WHERE a.actor_id = r.actor_id 
AND r.movie_id = m.movie_id #connections twn pinakwn
AND m.movie_id = md.movie_id
AND md.director_id = d.director_id
AND d.last_name = a.last_name
AND a.actor_id IN (
    SELECT DISTINCT r.actor_id
    FROM role r, movie m, movie_has_director md, director d
    WHERE r.movie_id = m.movie_id
    AND md.director_id = d.director_id
    AND m.movie_id = md.movie_id
    AND d.last_name <> a.last_name #to name tou director einai diaforetiko apo to name tou actor
    AND d.director_id IN (
        SELECT md2.director_id
        FROM movie_has_director md2, movie m2, movie_has_genre mg2, director d2
        WHERE md2.movie_id = m2.movie_id
        AND m2.movie_id = mg2.movie_id
        AND mg2.genre_id IN (
            SELECT DISTINCT mg.genre_id
            FROM movie_has_genre mg, movie m, movie_has_director md, director d
            WHERE mg.movie_id = m.movie_id
            AND m.movie_id = md.movie_id
            AND md.director_id = d.director_id
            AND d.last_name = a.last_name)
        AND d2.last_name <> a.last_name #eponymo d2 diaforetiko apo a 
        AND d2.director_id = md2.director_id)
);

#4
SELECT 'Yes' AS Answer
WHERE EXISTS (
    SELECT 1 #toulaxiston mia eggrafh pou pliroi thn sygkekrimenh synthiki
    FROM movie_has_genre mg, movie m
    WHERE mg.movie_id = m.movie_id
    AND mg.genre_id = (
        SELECT genre_id
        FROM genre
        WHERE genre_name = 'Drama') #compare genre_id me to genre_id ston movie_has_genre gia na doyme an h tainia einai drama.
    AND m.year = 1995 #tainia pou na exei gyristei to 95 
);


#5
SELECT DISTINCT d1.last_name AS director1_last_name, d2.last_name AS director2_last_name
FROM director d1, director d2
WHERE d1.director_id < d2.director_id
AND EXISTS (
	SELECT 1
	FROM movie_has_director md1, movie_has_director md2, movie m #copies zeygoi md1 kai md2 
	WHERE md1.director_id = d1.director_id
	AND md2.director_id = d2.director_id
	AND md1.movie_id = md2.movie_id
	AND md1.movie_id = m.movie_id
	AND m.year BETWEEN 2000 AND 2006) #na exoyn synskinothetisei thn idia tainia 
    AND (
        SELECT COUNT(DISTINCT mg1.genre_id)
        FROM movie_has_director md1, movie_has_director md2, movie_has_genre mg1, movie_has_genre mg2
        WHERE md1.director_id = d1.director_id
		AND md2.director_id = d2.director_id
		AND md1.movie_id = md2.movie_id
		AND md1.movie_id = mg1.movie_id
		AND md2.movie_id = mg2.movie_id ) >= 6; #if both directors exoyn skinothetisei 6 diaforetikes tainies apo 6 diaforetika gerne

#6
SELECT a.first_name, a.last_name, COUNT(DISTINCT md.director_id) AS count #count posoys different directors exoun oi tainies tou actor
FROM actor a, role r, movie_has_director md
WHERE a.actor_id = r.actor_id
AND r.movie_id = md.movie_id #connections 
AND r.actor_id IN (
	SELECT actor_id
	FROM role
	GROUP BY actor_id
	HAVING COUNT(*) = 3 ) #has played se akrivos 3 tainies 
GROUP BY a.actor_id, a.first_name, a.last_name;

#7
SELECT genre_id, COUNT(DISTINCT movie_id) AS count # count posoi directors exoun skinothetisei to genre
FROM movie_has_genre
WHERE genre_id IN (
	SELECT genre_id
	FROM movie_has_genre
	GROUP BY movie_id
	HAVING COUNT(*) = 1 ) #gia kathe tainia poy exei akribos ena eidos 
GROUP BY genre_id;

#8
SELECT actor_id
FROM actor
WHERE NOT EXISTS ( 
    SELECT genre_id
    FROM genre
    WHERE genre_id NOT IN (
        SELECT genre_id
        FROM movie_has_genre
        WHERE movie_has_genre.movie_id IN (
            SELECT movie_id
            FROM role
            WHERE role.actor_id = actor.actor_id)
	) #elenxoume an kapoio genre_id sto genre den anikei stis tainies pou paizei o actor
);

#9
SELECT genre1.genre_id  genre_id_1, genre2.genre_id  genre_id_2, COUNT(md.director_id) count #count directors poy exoyn skinothetisei movies kai twn 2 genre
FROM genre  genre1, genre  genre2, movie_has_genre  mg1, movie_has_genre  mg2, movie_has_director  md #kanoyme 2 copies genre1 kai genre2 kai mg1 kai mg2
WHERE genre1.genre_id = genre2.genre_id 
AND mg1.genre_id = genre1.genre_id
AND mg2.genre_id = genre2.genre_id
AND md.movie_id = mg1.movie_id 
AND md.movie_id = mg2.movie_id
GROUP BY genre_id_1, genre_id_2; #se kathe zeugos count tous directors pou exoun skinothetisei tainies kai twn dyo eidwn

#10
SELECT genre.genre_id AS genre, actor.actor_id AS actor, COUNT(*) AS count #to count o arithmos ton tainiwn ana eidos kai actor
FROM genre, actor, role, movie_has_genre
WHERE actor.actor_id = role.actor_id
AND role.movie_id = movie_has_genre.movie_id #connections
AND movie_has_genre.genre_id = genre.genre_id
AND NOT EXISTS (
    SELECT *
    FROM movie_has_director
    WHERE movie_has_director.movie_id = movie_has_genre.movie_id
    AND movie_has_director.director_id IN (
        SELECT DISTINCT director_id
        FROM movie_has_director AS mhd, movie_has_genre AS mg
        WHERE mhd.movie_id = mg.movie_id
        AND mg.genre_id != genre.genre_id) #an yparxei tainia me director pou na exei skinothetisei ki allo eidos
)
GROUP BY genre.genre_id, actor.actor_id;
