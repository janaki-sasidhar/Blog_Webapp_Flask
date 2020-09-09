from flask import Blueprint , flash , render_template , redirect , url_for , request , session
from flask_login import current_user , login_required , logout_user , login_user
from flask_blogg import db, bcrypt
from flask_blogg.models import Post , User , Plain
from flask_blogg.users.utils import send_reset_email
from datetime import datetime
from flask_blogg.users.forms import RegistrationForm , UpdateForm , LoginForm , RequestResetForm, ResetPasswordForm
users = Blueprint('users',__name__)


@users.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', title='Profile', user=user)


@users.route("/afterlogin", methods=['GET', 'POST'])
def afterlogin():
    if not current_user.is_authenticated:
        flash('You need to login first', 'danger')
        return redirect(url_for('users.login'))
    else:
        user = User.query.filter_by(username=current_user.username).first()
        posts = Post.query.filter_by(userid=user.id).all()
        return render_template("afterlogin.html", title="yass", user=user, posts=posts)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    session['name'] = form.username.data
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        # store plain text password.
        plain = Plain(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.add(plain)
        db.session.commit()
        flash(
            f'Account created for  user {form.username.data}. Please login', 'success')
        return redirect(url_for('users.login', name=session.get('name')))
    return render_template('register.html', form=form, title='Register')


@users.route("/loginForm", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Successfully logged in', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', form=form, title='Login')


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out Successfully', 'success')
    return redirect(url_for('users.login'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("The details have been updated successfully", "success")
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.email.data = current_user.email
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('account.html', title="Account", form=form, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to reset password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form, title='Reset password')


@users.route('/reset_password<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid token or may be expired', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        plain = Plain.query.filter_by(email=user.email).first()
        plain.password = form.password.data
        db.session.add(plain)
        db.session.commit()
        flash('Your password has been updated', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form, title='Reset password')
@users.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

