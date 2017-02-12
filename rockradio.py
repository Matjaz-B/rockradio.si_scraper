#!/usr/bin/python 

# -*- coding: utf-8 -*-

import requests
import sqlite3
import os
import pylast
import time


# "congif"
url = "http://rockradio.si/api/module/json/RadioSchedule/JsonModule/GetStreamInfo"
post = {'RadioStreamId': '1', 'SystemName': '', 'Title=': '', 'Description' : '',  'Icon%5BId%5D' : '0', 'Stream' : '', 'XmlStream' : '',  'Position' : '',  'Activated' : 'true'}
#curl -X POST -F 'RadioStreamId=1' -F 'SystemName=' -F 'Title=' -F 'Description=' -F 'Icon%5BId%5D=0' -F 'Stream=' -F 'XmlStream=' -F 'Position=' -F 'Activated=true'   
dbname = 'rockradio.db'

#lastfm
API_KEY = "??"
API_SECRET = "??"
username = "??"
password_hash = pylast.md5("??")

if os.path.isfile(dbname):
    conn = sqlite3.connect(dbname)
else:
    print "new db..."
    conn = sqlite3.connect(dbname)
    conn.execute('''CREATE TABLE PlayedSongs
       (artist  TEXT    NOT NULL,
       title    TEXT     NOT NULL,
       date     integer);''')
    conn.execute("insert into PlayedSongs Values (?, ?, strftime('%s', 'now')) ",  ("", ""));

    print "Table created"
        

r = requests.post(url, data=post)  
data = r.json()


print "Currently playing " + data['data'][0]['artist'].encode('utf-8') + " - " + data['data'][0]['title'].encode('utf-8')

cursor = conn.cursor()
row = cursor.execute('SELECT * FROM PlayedSongs ORDER BY date desc limit 1').fetchone()

if(data['data'][0]['artist'] == row[0] and data['data'][0]['title'] == row[1]):
    print "same song"
else:
    conn.execute("insert into PlayedSongs Values (?, ?, strftime('%s', 'now')) ",  (data['data'][0]['artist'], data['data'][0]['title']));
    conn.commit()
    #commit to lastfm
    if("ROCK RADIO" !=  data['data'][0]['title']):
        network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET, username = username, password_hash = password_hash)
        network.scrobble(artist=data['data'][0]['artist'], title=data['data'][0]['title'], timestamp=int(time.time()))



print "_____________________________\r\n\r\n"
for row in conn.execute('SELECT * FROM PlayedSongs ORDER BY date desc limit 10'):
        print row
        
conn.close()

