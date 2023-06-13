from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from werkzeug.security import check_password_hash, generate_password_hash
from sovaa.auth import login_required
from sovaa.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')

@bp.route('/profile/update_profile', methods=['POST'])
@login_required
def update_profile():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    username = request.form.get('username')
    if first_name and last_name:
        user_id = g.user['id']
        if user_id:
            db = get_db()
            db.execute(
                'UPDATE user SET username = ?, email = ?, first_name = ?, last_name = ?'
                ' WHERE id = ?',
                (username, email, first_name, last_name, user_id)
            )
            db.commit()
            flash('Profile successfully updated!', 'success')
        else:
            flash('User not found.', 'error')
    else:
        flash('Please provide a first name and last name.', 'error')
    return redirect(url_for('user.profile'))

@bp.route('/profile/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_password or not new_password or not confirm_password:
            flash('Please fill in all fields.', 'error')
        elif not check_password_hash(g.user['password'], current_password):
            flash('Incorrect current password.', 'error')
        elif new_password != confirm_password:
            flash('New password and confirmation password do not match.', 'error')
        else:
            db = get_db()
            hashed_password = generate_password_hash(new_password)
            db.execute(
                'UPDATE user SET password = ? WHERE id = ?',
                (hashed_password, g.user['id'])
            )
            db.commit()
            flash('Password successfully updated!', 'success')
            return redirect(url_for('user.profile'))

    return render_template('auth/change_password.html')