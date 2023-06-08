from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from main import db
from models import Note
import datetime
import json
from datetime import date
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

#landing page
@views.route('/')
def index():
    return render_template("home.html")

@views.route('/user-manual')
def user_manual():
    return render_template("user_manual.html")

@views.route('/code-of-conduct')
def code_of_conduct():
    return render_template("code_of_conduct.html")

#dashboard page
@views.route('/dashboard', methods=["GET", "POST"])
@login_required
def dash():
    if request.method == 'POST':
        #getting the users input for notes
        subject = request.form.get('subject')
        body = request.form.get('body')
        date = datetime.date.today()

        #parameters for note
        if len(subject) < 1:
            flash('subject is too short!', category='error')
        if len(body) < 1:
            flash('body is too short!', category='error')

        #creation of new note
        else:
            new_note = Note(subject=subject, body=body,  date=date, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note successfully Created!', category='success')
            return redirect(url_for('views.dash'))
            
    return render_template("dash.html", user=current_user)

#user data page
@views.route('/user-data', methods=["GET", "POST"])
@login_required
def user_data():
    return render_template("user_data.html", user=current_user)

#history page
@views.route('/history')
@login_required
def history():
    return render_template("history.html", user=current_user)

#deleting of a note from database
@views.route('/delete-note', methods=["POST"])
def delete_note():
    #converting note value to python string
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        #deleting user note
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})