from flask import Blueprint, request, render_template, session, redirect, url_for, flash

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def is_logegd():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    return render_template('admin.html')


# Create Login Page
@admin.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        if request.form.get('user') == "admin" and request.form.get('pw') == "12345":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash('Incorrect password or Login')

    return render_template('admin_login.html')


@admin.route('/logout', methods=['POST', 'GET'])
def logout():
    if not is_logegd():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))
