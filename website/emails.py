from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from flask_login import current_user
from main import db
from flask_mail import Mail, Message


emails = Blueprint('emails', __name__)
app = Flask(__name__)
#configuration for mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'signupsystemmdp@gmail.com'
app.config['MAIL_PASSWORD'] = 'lgzblbzwfhzcubrq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)
mail.init_app(app)

#forgot password email
@emails.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    link = redirect(url_for('auth.reset_password'))
    if request.method == "POST":
        email = request.form.get('email-address')
        #email to be sent
        msg = Message('Forgot Password', sender='signupsystemmdp@gmail.com', recipients=[email])
        msg.html = render_template('reset_password_email.html', link=link)
        mail.send(msg)
        flash('Reset password email has been sent! Please check your emails.')

    return render_template('forgot_password.html', user=current_user)
