from typing import List, Dict
from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import json
from flask_basicauth import BasicAuth
import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import sys

app = Flask(__name__)
app.secret_key = "secret key"
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

config = {
    'user': 'root',
    'password': 'root',
    'host': 'database',
    'port': '3306',
    'database': 'timetable'
}

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('/home', filename))

        flash('File(s) successfully uploaded')
        file_path = '/home/' + filename

        f = open(file_path, 'r')
        name = f.readline()
        prog_name = f.readline()
        actual_timetable = f.read()

        create_if_not_existent = 'CREATE TABLE IF NOT EXISTS timetable_pending (person_name VARCHAR(20), timetable_name VARCHAR(20), actual_restrictions TEXT );'
        cursor.execute(create_if_not_existent)
        cursor.execute("COMMIT")

        query = "INSERT INTO timetable_pending (person_name, timetable_name, actual_restrictions) VALUES (%s,%s,%s)"
        args =(name.replace('\n', ''), prog_name.replace('\n', ''), actual_timetable)
        cursor.execute(query, args)
        cursor.execute("COMMIT")
        return redirect('/')

@app.route('/print/<table>')
def find_table(table):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table)
    results = [var for var in cursor]
    cursor.close()
    connection.close()
    return str(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
