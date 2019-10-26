import requests
import pymongo
from pymongo import MongoClient
from flask import Flask, jsonify, request
from datetime import datetime
from datetime import timedelta
import uuid, json
import dateutil.parser as parser
import hashlib, traceback
import dns

client = pymongo.MongoClient("mongodb://URL")
db = client.lsrdb

class DatabaseManager:

    def saveData(self, localMap):
        try:
            connect = db.stats
            connect.insert(localMap)
            return jsonify({"status":"success"})
        except:
            print(traceback.format_exc())
            return jsonify({"status":"failed"})
            
    def saveuser(self, localMap):
        try:
            connect = db.users
            connect.insert(localMap)
            return jsonify({"status":"success"})
        except:
            print(traceback.format_exc())
            return jsonify({"status":"failed"})

    def getData(self, user, timefrom, timeto):
        connect = db.stats
        query = {'user':user, 'time': {'$gte': int(timefrom), '$lt': int(timeto)}}
        print(query)
        mapResp = []
        for q in connect.find(query, {'_id': False}):
            mapResp.append(q)
        return jsonify({"status":"success",'data':mapResp})

    
    def getuser(self, user):
        connect = db.users
        query = {'user':user}
        resp = {}
        for q in connect.find(query, {'_id': False}):
            resp = q
        return resp