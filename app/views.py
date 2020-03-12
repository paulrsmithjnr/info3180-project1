"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import ProfileForm
from app.models import Profile
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    """Render the website's profile page."""
    profilePage = ProfileForm()

    if request.method == 'POST':
        if profilePage.validate_on_submit():

            firstName = profilePage.firstName.data
            lastName = profilePage.lastName.data
            gender = profilePage.gender.data
            email = profilePage.email.data
            location = profilePage.location.data
            biography = profilePage.biography.data
            photo = profilePage.photo.data

            filename = secure_filename(photo.filename)
            photo.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename
            ))

            profile = Profile(first_name=firstName, last_name=lastName, gender=gender, email=email, location=location, biography=biography, profile_picture=filename)
            db.session.add(profile)
            db.session.commit()

            flash('New Profile Created!', 'success')
            return redirect(url_for('profiles'))
        else:
            flash_errors(profilePage)

    return render_template('profile.html', form = profilePage)

@app.route('/profiles')
def profiles():
    """Render the website's profiles page."""
    return render_template('profiles.html')

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if request.method == "POST":
#         # change this to actually validate the entire form submission
#         # and not just one field
#         if form.validate_on_submit():
#             # Get the username and password values from the form.
#             username = form.username.data
#             password = form.password.data

#             # using your model, query database for a user based on the username
#             # and password submitted. Remember you need to compare the password hash.
#             # You will need to import the appropriate function to do so.
#             # Then store the result of that query to a `user` variable so it can be
#             # passed to the login_user() method below.

#             user = UserProfile.query.filter_by(username=username).first()

#             if user is not None and check_password_hash(user.password, password):

#                 # get user id, load into session
#                 login_user(user)

#                 # remember to flash a message to the user
#                 flash('Logged in successfully.', 'success')
#                 return redirect(url_for("secure_page"))  # they should be redirected to a secure-page route instead
#     return render_template("login.html", form=form)




# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return Profile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
