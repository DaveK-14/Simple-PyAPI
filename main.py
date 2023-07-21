import logging
from flask import Flask, request, jsonify
from database.database import db_connect, Base
from sqlalchemy.orm import Session
from models.Event import Event
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)

engine = db_connect(os.getenv('user'), os.getenv('password'), os.getenv('location'), str(os.getenv('port')), os.getenv('dbName'))

def init_db(engine):
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.commit()
        session.close()

@app.route('/pulse/', methods = ['GET'])
def pulse():
    return "Running", 200

@app.route('/', methods = ['POST'])
def add():
    with Session(engine) as session:
        try:
            event = Event.fromJSON(request.json)
            if event is list:
                session.add_all(event)
            else:
                session.add(event)
            session.commit()
        except Exception as e:
            session.rollback()
            session.close()
            print(e)
            return "Request failed", 400
        session.close()
    return "Accepted", 201

@app.route('/view/', methods = ['GET'])
def view():
    data = request.json
    events = []
    with Session(engine) as session:
        try:
            query = session.query(Event).where(Event.id == data["id"])
            for row in query:
                events.append(row.toJSON())
        except Exception as e:
            session.rollback()
            session.close()
            print(e)
            return "Request failed", 400
        session.close()
    return jsonify(events), 200

@app.route('/search/<keyword>/', methods = ['GET'])
def search(keyword):
    data = request.json
    events = []
    with Session(engine) as session:
        try:
            if keyword == "client":

                query = session.query(Event).where(Event.client.contains(data["client"]))
                for row in query:
                    events.append(row.toJSON())
            elif keyword == "description":
                query = session.query(Event).filter(Event.description.contains(data["description"]))
                for row in query:
                    events.append(row.toJSON())
            elif keyword == "creator":
                query = session.query(Event).filter(Event.createdBy == data["createdBy"])
                for row in query:
                    events.append(row.toJSON())
            else:
                return "Invalid keyword. Please use 'client' or 'description'."
        except Exception as e:
            session.rollback()
            session.close()
            print(e)
            return "Request failed", 400
    session.close()
    return jsonify(events), 200
        

@app.route('/delete/', methods = ['DELETE'])
def delete():
    data = request.json
    with Session(engine) as session:
        try:
            if data is list:
                for id in data:
                    event = session.query(Event).filter(Event.id == id["id"])
                    session.delete(event[0])
            else:
                event = session.query(Event).filter(Event.id == data["id"])
                session.delete(event[0])
            session.commit()
        except Exception as e:
            session.rollback()
            session.close()
            print(e)
            return "Request failed", 400
        session.close()
    return "Deleted", 200

if __name__ == '__main__':
    init_db(engine)
    app.run(debug = True)
