import sys, random, time, json
from optparse import OptionParser
import requests

baseurl = "http://18.222.209.47:5000"
HEADERS_USER = {'Content-type': 'application/json'}

def runall():
    sessurl = baseurl + "/saveStats"
    config = {"user":"abc","rpm":random.randint(10, 30), "distance":random.random(),"signal":random.random()} 
    rv = requests.post(sessurl, data=json.dumps(config), headers=HEADERS_USER)
    time.sleep(1)
    runall()

runall()