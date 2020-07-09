from flask import render_template, redirect, url_for, session
from flask_login import logout_user, login_required
from app.user import user
from flask import Markup



@user.route('/profile')
@login_required
def profile():
	return render_template('user/profile.html', email=session['user-email'], user_name=session['user-name'], table_data=Markup(session['table-data']), user_image=session['user-image'])


@user.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user-email') #deteting the variable at end of session
    return redirect(url_for('home.start'))
