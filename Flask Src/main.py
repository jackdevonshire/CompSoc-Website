from flask import Flask, request, jsonify, render_template
import sqlite3
import os

AUTH_TOKEN = "A SECURE TOKEN HERE"
app = Flask(__name__)

application = app

links = []
events = []
conn = sqlite3.connect("site.db")
cursor = conn.cursor()

cursor.execute("SELECT Icon, Title, Description, Link, Featured FROM Links")
for link in cursor.fetchall():
    links.append({
        "icon": link[0],
        "title": link[1],
        "description": link[2],
        "link": link[3],
        "featured": link[4]
    })
cursor.execute("SELECT Date, Description, Link, Featured FROM Events")
for event in cursor.fetchall():
    events.append({
        "date": event[0],
        "description": event[1],
        "link": event[2],
        "featured": event[3]
    })

conn.close()

@app.route('/', methods=["GET"])
def home():
    return render_template('index.html', links=links, events=events)

@app.route('/api/content', methods=["POST"])
def update_content():
    global events
    global links

    data = request.get_json()

    if data["token"] != AUTH_TOKEN:
        response = jsonify({'message': 'Failed auth'})
        return response

    events = data["events"]
    links = data["links"]

    conn = sqlite3.connect("site.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Events")
    cursor.execute("DELETE FROM Links")

    for event in events:
        cursor.execute("INSERT INTO Events (Date, Description, Link, Featured) VALUES (?,?,?,?)",
                       (event["date"], event["description"], event["link"], event["featured"]))
    for link in links:
        cursor.execute("INSERT INTO Links (Icon, Title, Description, Link, Featured) VALUES (?,?,?,?,?)",
                       (link["icon"], link["title"], link["description"], link["link"], link["featured"]))
    conn.commit()
    conn.close()

    response = jsonify({'message': 'Updated links and events'})
    return response

if __name__ == "__main__":
    app.run()