from flask import Flask
from flask import render_template

app=Flask(__name__, template_folder="templates/")

@app.route("/")
def index():
    return render_template("index.html", title="Index")

if __name__ == '__main__':
    app.run(debug=True) 