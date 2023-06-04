from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from sovaa.auth import login_required
from sovaa.db import get_db

bp = Blueprint('auction', __name__)


@bp.route('/')
def general():
    db = get_db()
    announcements = db.execute(
        'SELECT a.id, title, body, created, author_id, username'
        ' FROM announcement a JOIN user u ON a.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('auction/index.html', announcements=announcements)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        price = request.form['price']
        image = request.files['images']
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
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)

            db = get_db()
            db.execute(
                'INSERT INTO announcement (title, body, price, author_id, images)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, price, g.user['id'], image_path)
            )
            db.commit()
            return redirect(url_for('auction.general'))

    return render_template('auction/create.html')


def get_announcement(id, check_author=True):
    announcement = get_db().execute(
        'SELECT a.id, title, body, price, created, author_id, username'
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
            return redirect(url_for('auction.general'))

    return render_template('auction/update.html')


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_announcement(id)
    db = get_db()
    db.execute('DELETE FROM announcement WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('auction.general'))

