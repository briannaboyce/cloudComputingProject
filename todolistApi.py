# This is a simple example web app that is meant to illustrate the basics.
from flask import Flask, render_template, redirect, g, request, url_for
import sqlite3
import json

DATABASE = 'todolist.db'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/api/items")
def get_items():
    db = get_db()
    cur = db.execute('SELECT what_to_do, due_date, status FROM entries')
    entries = cur.fetchall()
    tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2])
              for row in entries]
    return json.dumps(tdlist)

@app.route("/api/items/add", methods=['POST'])
def add_entry():
	db = get_db()
	print(dir(request))
	print(" ")
	print(dir(request.form))
	print(" ")
	print(dir(request.json))
	print(" ")
	print(dir(request.data))

	db.execute('insert into entries (what_to_do, due_date) values (?, ?)',
			   [request.json['whatToDo'], request.json['dueDate']])
	db.commit()
	response = {
		"status": "200"
	}
	return json.dumps(response) #redirect(url_for('show_list'))

@app.route("/api/items/delete/<item>")
def delete_entry(item):
	db = get_db()
	print('deleting '+item)
	db.execute("DELETE FROM entries WHERE what_to_do='"+item+"'")
	db.commit()
	response = {
		"status": "200"
	}
	return  json.dumps(response) #redirect(url_for('show_list'))

@app.route("//api/items/mark/<item>")
def mark_as_done(item):
	db = get_db()
	db.execute("UPDATE entries SET status='done' WHERE what_to_do='"+item+"'")
	db.commit()
	response = {
		"status": "200"
	}
	return json.dumps(response)#redirect(url_for('show_list'))

def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
	return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request."""
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

if __name__ == "__main__":
	app.run("0.0.0.0")
