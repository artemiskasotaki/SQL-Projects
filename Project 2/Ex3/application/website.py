import sys, os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
from bottle import route, run, static_file, request
import pymysql as db
import settings  # Αυτό πρέπει να λειτουργεί αν το settings.py είναι στον ίδιο φάκελο

import app

def renderTable(tuples):
    printResult = """<style type='text/css'> h1 {color:red;} h2 {color:blue;} p {color:green;} </style>
    <table border = '1' frame = 'above'>"""
    header = '<tr><th>'+'</th><th>'.join([str(x) for x in tuples[0]])+'</th></tr>'
    data = '<tr>'+'</tr><tr>'.join(['<td>'+'</td><td>'.join([str(y) for y in row])+'</td>' for row in tuples[1:]])+'</tr>'
    printResult += header + data + "</table>"
    return printResult

@route('/updateRank')
def updateRank():
    r1 = request.query.rank1 or "Unknown Rank"
    r2 = request.query.rank2 or "Unknown Rank"
    mtitle = request.query.movieTitle or "Unknown Title"
    table = app.updateRank(r1, r2, mtitle)
    return "<html><body>" + renderTable(table) + "</body></html>"

@route('/colleaguesOfColleagues')
def colleaguesOfColleagues():
    aid1 = request.query.actorId1
    aid2 = request.query.actorId2
    table = app.colleaguesOfColleagues(aid1, aid2)
    return "<html><body>" + renderTable(table) + "</body></html>"

@route('/actorPairs')
def actorPairs():
    aid = request.query.actorId
    table = app.actorPairs(aid)
    return "<html><body>" + renderTable(table) + "</body></html>"

@route('/selectTopNactors')
def selectTopNactors():
    try:
        n = int(request.query.n)
    except ValueError:
        return "<html><body>Invalid value for n</body></html>"
    table = app.selectTopNactors(n)
    return "<html><body>" + renderTable(table) + "</body></html>"

@route('/traceActorInfluence')
def traceActorInfluence():
    aid = request.query.actorId
    table = app.traceActorInfluence(aid)
    return "<html><body>" + renderTable(table) + "</body></html>"

@route('/:path')
def callback(path):
    return static_file(path, 'web')

@route('/')
def callback():
    return static_file("index.html", 'web')

run(host='localhost', port=settings.web_port, reloader=True, debug=True)
