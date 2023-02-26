# import requirements

import requests
from flask import Flask, render_template, request, redirect
import psycopg2


# app created

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="password",
                        host="localhost",
                        port="5433")

cursor = conn.cursor()


# add decorator

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if records:
        return render_template('account.html', full_name=records[0][1], username = username, password = password)
    else:
        return render_template('no_user.html')


