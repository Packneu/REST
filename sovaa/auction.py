import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from sovaa.auth import login_required
from sovaa.db import get_db

bp = Blueprint('auction', __name__)

UPLOAD_FOLDER = 'sovaa/static/images'
PUBLIC_FOLDER = 'images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    db = get_db()
    announcements = db.execute(
        'SELECT a.id, title, body, price, created, author_id, username, images'
        ' FROM announcement a JOIN user u ON a.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('auction/index.html', announcements=announcements)


@bp.route('/created', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        price = request.form['price']
        image = request.files['image']
        error = None

        if not title:
            error = 'Title is required.'

        if not price:
            error = 'Price is required.'

        if not image or not allowed_file(image.filename):
            error = 'Invalid image file. Allowed file types are jpg, jpeg, png, and gif.'

        if error is not None:
            flash(error)
        else:
            filename = secure_filename(image.filename)
            image_path = os.path.join(PUBLIC_FOLDER, filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))

            db = get_db()
            db.execute(
                'INSERT INTO announcement(title, body, price, author_id, images)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, price, g.user['id'], image_path)
            )
            db.commit()
            return redirect(url_for('auction.index'))

    return render_template('auction/create.html')


def get_announcement(id, check_author=True):
    announcement = get_db().execute(
        'SELECT a.id, title, body, price, created, author_id, username, images'
        ' FROM announcement a JOIN user u ON a.author_id = u.id'
        ' WHERE a.id = ?',
        (id,)
    ).fetchone()

    if announcement is None:
        abort(404, f"Announcement id {id} doesn't exist.")

    if check_author and announcement['author_id'] != g.user['id']:
        abort(403)

    return announcement


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    announcement = get_announcement(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        price = request.form['price']
        error = None

        if not title:
            error = 'Title is required.'

        if not price:
            error = 'Price is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE announcement SET title = ?, body = ?, price = ?'
                ' WHERE id = ?',
                (title, body, price, id)
            )
            db.commit()
            return redirect(url_for('auction.index'))

    return render_template('auction/update.html')


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_announcement(id)
    db = get_db()
    db.execute('DELETE FROM announcement WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('auction.index'))

