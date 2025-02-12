from flask import Flask, render_template, url_for, send_file, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations.db'  # SQLite database file
db = SQLAlchemy(app)

auth = HTTPBasicAuth()

# Define the Registration model
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    pax = db.Column(db.Integer, nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

admins = {
    "denhafiz": "haha"
}

data = {
    'groom': 'Den Hafiz',
    'bride': 'Nor Syazni',
    'fullgroom': 'Den Muhammad Hafiz Bin Jumaatuden',
    'fullbride': 'Nor Syazni Binti Mazlan', 
    'father': 'Mazlan Bin Abdullah',
    'mother': 'Noriza Binti Ahmad',
    'date': '14 Jun 2025',
    'day': 'Sabtu',
    'time': '11:00 Pagi - 04:00 Petang',
    'firstaddress': 'Kampung Bukit Kelidang, Gual Ipoh,',
    'secondaddress': '17500 Tanah Merah, Kelantan',
    'location' : 'Tanah Merah, Kelantan'
}

@app.route("/")
def index():
    return render_template("index.html", data=data)

@app.route("/home", methods=['GET'])
def home():
    # return send_file("templates/_home.html", mimetype="text/html")
    return render_template("_home.html", data=data)


@app.route("/rsvp", methods=['POST'])
def rsvp():
    name = request.form.get('name')
    phone = request.form.get('phone')
    pax = request.form.get('pax')

    print(f"--- User {name} has been registered for {pax} people. ---")

    # Save the data to the database
    new_registration = Registration(name=name, phone=phone, pax=pax)
    db.session.add(new_registration)
    db.session.commit()

    return "Success"



#####################
# Admin Stuff Below #
#####################

@auth.verify_password
def verify_password(username, password):
    if username in admins and admins[username] == password:
        return username

@app.route('/clear-data', methods=['POST'])
def clear_data():
    # Delete all records from Registration table
    db.session.query(Registration).delete()
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin')
@auth.login_required
def admin():
    # Fetch all registration from the database
    registrations = Registration.query.all()
    return render_template('admin.html', registrations=registrations)

if __name__ == '__main__':  
   app.run(debug=True)  