from flask import Flask, render_template, url_for, send_file, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

import csv

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

    success_message = "<p class='success-message'>Terima kasih kerana mendaftar.<br> Maklumat anda telah disimpan.</p>"

    return success_message



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


@app.route('/download-csv', methods=['POST'])
def download_csv():
    # Put all data in database into a csv
    registrations = Registration.query.all()

    csv_path = 'registrations.csv'  # Or a more dynamic path if needed
    registration_list = []

    for registration in registrations:
        registration_list.append([
            registration.id,
            registration.name,
            registration.phone,
            registration.pax
        ])

    with open(csv_path, mode='w', newline='', encoding='utf-8') as file: # Add encoding for special characters
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Phone", "Pax"]) # Write header row
        writer.writerows(registration_list) 
        
    directory = '.' # or 'static' if you put data.csv there
    return send_from_directory(
        directory=directory, 
        path=csv_path,
        mimetype='text/csv',  # Important for proper handling by browsers
        as_attachment=True  # Forces the browser to download the file
    )

@app.route('/admin')
@auth.login_required
def admin():
    # Fetch all registration from the database
    registrations = Registration.query.all()
    return render_template('admin.html', registrations=registrations)

if __name__ == '__main__':  
   app.run(debug=True)  