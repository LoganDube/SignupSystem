from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User
from main import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

#user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        #users input
        email = request.form.get('email')
        password = request.form.get('password')
        
        #check email validity
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.dash'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('login.html', user=current_user)

#user log out
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))
    #redirect to index page


#user sign up
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        #users input
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #parameters of signing up
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('Name must be character than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        else:
            #add user to database
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method="sha256")) #sha256 is a hashing algorithm
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.dash'))

    return render_template('signup.html', user=current_user)

#user change password
@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == "POST":
        #users input
        email = request.form.get('email-address')
        new_password = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            #changing password
            user.password = generate_password_hash(new_password, method="sha256")
            db.session.commit()
            flash('Password Successfully Changed!', category='success')            
            return redirect(url_for('auth.login'))

        else:
            #parameters of new password
            if User.email != email:
                flash('Email does not exist.', category='error')
            elif new_password != password2:
                 flash('Passwords don\'t match', category='error')

    return render_template('reset_password.html')

#user change data
@auth.route('/change-user-data', methods=['GET', 'POST'])
def change_user_data():
    if request.method == "POST":
        #user input + current data from database
        new_email = request.form.get('email')
        new_name = request.form.get('name')
        email = User.email
        
        user = User.query.filter_by(email=email).first()
        if user:
            #changing only one value
            if len(new_email) <1:
                if len(new_name) <1:
                    flash('There were no new inputs, account information stays the same.', category='error')
                    return redirect(url_for('views.user_data'))
                else:
                    user.name = new_name
                    db.session.commit()
                    flash('Details Successfully Updated!', category='success')
                    return redirect(url_for('views.user_data'))
            elif len(new_name) < 1:
                user.email = new_email
                db.session.commit()
                flash('Details Successfully Updated!', category='success')
                return redirect(url_for('views.user_data'))

            else:
                #changing of database
                user.email = new_email
                user.name = new_name
                db.session.commit()
                flash('Details Successfully Updated!', category='success')
                return redirect(url_for('views.user_data')) 
        else:  
            #parameters of changing user data
            if len(new_email) < 3 :
                flash('Email Too Short.', category='error')
            if len(new_name) < 2 :
                flash('Name Too Short.', category='error')         
        
    return render_template("change_user_data.html", user=current_user)