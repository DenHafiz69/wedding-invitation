from flask import Flask
from flask import render_template, redirect, request

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app=Flask(__name__, template_folder="templates/")

data = {
    "groom": "Den Hafiz",
    "bride": "Nor Syazni",
    "date": "14th June 2025"
}

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html", data=data, hidden=True)


@app.route('/rsvp', methods=['POST'])
def rsvp():

    if request.method == 'POST':
        # Get the values from HTML page
        user_name = request.form['name']
        user_phone = request.form['phone']
        user_pax = request.form['pax']

        print(f"User {user_name} has registered.")

        return render_template('index.html', data=data, hidden=False)

if __name__ == '__main__':
    app.run(debug=True)