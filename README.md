# Wedding Invitation App

This Flask application is a wedding invitation website with an RSVP form. Users can submit their RSVP information, which is then stored in a database.

## Project Structure

    - app.py: The main Flask application file.
    - templates:
        - base.html: The base template for all other HTML templates.
        - contact.html: A contact page.
        - index.html: The homepage of the wedding website.
        - location.html: A page with information about the wedding location.
        - rsvp.html: The RSVP form page.
        - success.html: A confirmation page displayed after successful RSVP submission.
        - tentative.html: A page displayed if the user RSVPs as tentative.
    - static:
        - styles.css: Stylesheets for the website.

## To-Do List

    - Integrate the RSVP form with a database to store user information.