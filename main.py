#!flask/bin/python
"""`main` is the top level module for your Flask application."""
from __future__ import absolute_import
import logging, traceback
from flask import Flask, redirect, send_file, request, json, Response, jsonify
import os
app = Flask(__name__)
from db import DatabaseManager
import time
from twilio.rest import Client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import base64

db = DatabaseManager()

@app.route('/', methods=['GET'])
@app.route('/register', methods=['GET'])
def get_main():
    try:
        return send_file('main.html')
    except Exception as e:
        return str(e)

@app.route('/login', methods=['GET'])
def login():
    try:
        return send_file('login.html')
    except Exception as e:
        return str(e)

@app.route('/officemode', methods=['GET'])
def officemode():
    try:
        return send_file('officemode.html')
    except Exception as e:
        return str(e)

@app.route('/profile', methods=['GET'])
def get_loggedin():
    try:
        return send_file('profile.html')
    except Exception as e:
        return str(e)

@app.route('/saveuser', methods=['POST'])
def saveuser():
    try:
        data = request.get_json(silent=True)
        print(data)
        localmap = {}
        localmap['user'] = data['user']
        localmap['email'] = data['email']
        localmap['phone'] = data['phone']
        localmap['friendemail'] = data['friendemail']
        localmap['friendphone'] = data['friendphone']
        localmap['docemail'] = data['docemail']
        localmap['docphone'] = data['docphone']
        status = db.saveuser(localmap)
        return status
    except:
        print(traceback.format_exc())
        return jsonify({"status":"failed", "result":"failed to save user"})

@app.route('/saveStats', methods=['POST'])
def saveStats():
    try:
        data = request.get_json(silent=True)
        localmap = {}
        localmap['user'] = data['user']
        localmap['rpm'] = data['rpm']
        localmap['distance'] = data['distance']
        localmap['time'] = int(time.time())
        status = db.saveData(localmap)
        sender = 'ajesh12k@gmail.com'
        if data['rpm'] > 50:
            userinfo = db.getuser(data['user'])
            docnumber = userinfo['docphone']
            docemail = userinfo['docemail']
            sendsms(docnumber, "Your patient {} seems to be stressed".format(data['user']))
            sendmail(sender, docemail, data['user'] + " is stressed", "Seems like your patient {} is stressed".format(data['user']))
        if data['rpm'] > 40:
            userinfo = db.getuser(data['user'])
            friendnumber = userinfo['friendphone']
            friendemail = userinfo['friendemail']
            sendsms(friendnumber, "Your friend {} seems to be stressed".format(data['user']))
            sendmail(sender, friendemail, data['user'] + " is stressed", "Seems like your friend {} is stressed".format(data['user']))
        if data['rpm'] > 30:
            userinfo = db.getuser(data['user'])
            print(userinfo)
            phone = userinfo['phone']
            email = userinfo['email']
            sendsms(phone, "You seem to be stressed")
            sendmail(sender, email, data['user'] + " is stressed", "Seems like you are stressed")
        return jsonify({"status":"success"})
    except:
        print(traceback.format_exc())
        return jsonify({"status":"failed"})

@app.route('/getallusers', methods=['GET'])
def getallusers():
    try:
        return db.getallusers()
    except:
        return jsonify({"status":"failed"})

@app.route('/getData', methods=['GET'])
def getData():
    try:
        user = request.args.get("user")
        fromtime = request.args.get("from")
        totime = request.args.get("to")
        print(user, fromtime, totime)
        data = db.getData(user, fromtime, totime)
        return data
    except:
        print(traceback.format_exc())
        return jsonify({"status":"failed"})

def sendsms(number, message):
    try:
        account_sid = "ACd2be1e72472c2c271f4851048445eaf6"
        auth_token  = "439bbdd82f5de7b7093be4082a064ed6"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
                    to=number, 
                    from_="+12564108789",
                    body=message)
        print(message.error_code)
        if not message.error_code:
            return json.dumps({"success":True, "status":"Sent SMS", "error":None})
    except Exception as e:
        logging.debug("Error sending SMS - {}".format(e))
        return json.dumps({"success":False, "status":"Error sending SMS"})

def sendmail(sender, to, subject, message_text):
    import os
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    message = Mail(
        from_email=sender,
        to_emails=to,
        subject=subject,
        html_content='<strong>{}</strong>'.format(message_text))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 5000)))
