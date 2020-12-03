from flask import Blueprint, flash, render_template, redirect, abort, request, abort, url_for
from flask_login import current_user, login_required
from flask_blogg.models import Post
from flask_blogg import db
import datetime
from flask_blogg.posts.forms import PostForm, PostUpdateForm
posts = Blueprint('posts', __name__)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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
            post.last_modified = datetime.datetime.utcnow()
            db.session.add(post)
            db.session.commit()
            flash('Your post has been updated successfully', "success")
            return redirect(url_for('main.index'))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
            return render_template('update_post.html', post=post, form=form)


@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, userid=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('The post has been created successfully', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Post', form=form)
