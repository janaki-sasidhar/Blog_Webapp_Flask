from flask import flash, redirect, url_for, session, request, abort
from flask import render_template
from flask_blogg.forms import RegistrationForm, LoginForm, UpdateForm, PostForm, PostUpdateForm
from flask_blogg.models import User, Post, Plain
from flask_blogg import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        return render_template('index.html', posts=posts, title='Index', user=user)
    else:
        return render_template('index.html', posts=posts, title='Index')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', title='Profile', user=user)


@app.route("/afterlogin", methods=['GET', 'POST'])
def afterlogin():
    if not current_user.is_authenticated:
        flash('You need to login first', 'danger')
        return redirect(url_for('login'))
    else:
        user = User.query.filter_by(username=current_user.username).first()
        posts = Post.query.filter_by(userid=user.id).all()
        return render_template("afterlogin.html", title="yass", user=user, posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
        return redirect(url_for('login', name=session.get('name')))
    return render_template('register.html', form=form, title='Register')


@app.route("/loginForm", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
                return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('Login.html', form=form, title='Login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out Successfully', 'success')
    return redirect(url_for('login'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("The details have been updated successfully", "success")
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.email.data = current_user.email
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('account.html', title="Account", form=form, user=user)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    else:
        form = PostUpdateForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.add(post)
            db.session.commit()
            flash('Your post has been updated successfully', "success")
            return redirect(url_for('index'))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
            return render_template('update_post.html', post=post, form=form)


@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, userid=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('The post has been created successfully', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post', form=form)


@app.errorhandler(404)
def error_404(e):
    return render_template("400.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
