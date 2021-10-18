from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import datetime
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/sms'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'hi'

db = SQLAlchemy(app)

def generate_uuid():
    return str(uuid.uuid4())

class MessageLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderPhone = db.Column(db.String(20), nullable=False)
    receiverPhone = db.Column(db.String(20), nullable=False)
    messageText = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    uuid = db.Column(db.String(100), name="uuid", default=generate_uuid)

    def __init__(self, senderPhone, receiverPhone, messageText):
        self.senderPhone = senderPhone
        self.receiverPhone = receiverPhone
        self.messageText = messageText



@app.route('/')
def home():
    return '<a href="/sendSMSMessage"><button> Click To Send SMS </button></a> <a href="/viewSMSMessage"><button> Click To Show SMS</button></a>'


@app.route("/sendSMSMessage")
def sendSMSMessage():
    return render_template("index.html")

@app.route("/viewSMSMessage")
def viewSMSMessage():
    return render_template("view_sms.html")


@app.route("/sendSMS", methods=['POST'])
def sendSMS():
    senderPhone = request.form["senderPhone"]
    receiverPhone = request.form["receiverPhone"]
    messageText = request.form["messageText"]
    entry = MessageLog(senderPhone, receiverPhone, messageText)
    db.session.add(entry)
    db.session.commit()
    return {"status": "success", "message": "Message Sent Successfully"}

@app.route("/viewSMS", methods=['POST'])
def viewSMS():
    senderPhone = request.form["senderPhone"]
    receiverPhone = request.form["receiverPhone"]
    message_log = MessageLog.query.filter(or_(senderPhone == senderPhone, receiverPhone == receiverPhone)).first()
    return {"status": "success", "Sender Phone": message_log.senderPhone, "Reciever Phone": message_log.receiverPhone, "Message": message_log.messageText, "Time": message_log.timestamp}

if __name__ == '__main__':
    db.create_all()
    app.run()