from flask_blogg import mail 
from flask import url_for , current_app
from flask_mail import Message

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f'''
To reset your password , visit the following link.
{url_for('users.reset_password',token=token , _external=True)}
If you didnt make request, ignore it.
'''
    mail.send(msg)


