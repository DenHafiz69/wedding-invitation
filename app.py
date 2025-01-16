from flask import Flask
from flask import render_template, redirect, request

app=Flask(__name__, template_folder="templates/")

data = {
    "groom": "Den Hafiz",
    "bride": "Nor Syazni",
    "date": "14th June 2025"
}

@app.route('/')
def index():
    return render_template("index.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)