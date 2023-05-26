from flask import Blueprint, redirect, render_template, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('fname')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!!!', category='error')
        if len(email) < 7:
            flash('Email invalid', category='error')
        elif len(fname) < 2:
            flash('Name too short, should be more than 2', category='error')
        elif len(password) < 8:
            flash('Password too short, should be 8 characters', category='error')
        elif password != passwordConfirm:
            flash('Password not confirmed correctly', category='error')
        else:
            user = User(email=email, first_name=fname, password=generate_password_hash(password, method='sha256'))
            db.session.add(user)
            db.session.commit()

            flash('Account Successfully Created!!!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
    return render_template('signup.html', user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Succesfully !!!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Login Failed !!!', category='error')
        else:
            flash('Email doesnt exists, Signup first!!!', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
