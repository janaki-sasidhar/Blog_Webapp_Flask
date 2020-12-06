from flask import Blueprint, flash, render_template, redirect, abort, request, abort, url_for
from flask_login import current_user, login_required
from flask_blogg.models import Paste
from flask_blogg import db
import datetime
from flask_blogg.paste.forms import PasteForm
paste = Blueprint('paste', __name__)


@paste.route('/paste/new', methods=['GET', 'POST'])
@login_required
def new_paste():
    form = PasteForm()
    if form.validate_on_submit():
        paste = Paste(title=form.title.data,
                      content=form.content.data, userid=current_user.id)
        db.session.add(paste)
        db.session.commit()
        flash('The paste has been created successfully', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_paste.html', title='New Paste', form=form)


@paste.route('/paste/<title>', methods=['GET', 'POST'])
def view_paste(title):
    paste = Paste.query.filter_by(title=title).first()
    if paste:
        paste_data = paste
        title = paste_data.title
    else:
        paste_data = 'Your Paste has been deleted!'
        title = 'Oops !'

    return render_template('view_paste.html',  paste_data=paste_data, title=title)
