from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
# from flask_mail import Message
# from . import mail
# from random import randint
import re

emailregex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist. Please sign up to continue.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif not re.fullmatch(emailregex, email):
            flash('Please enter valid email.', category='error')
        elif len(first_name) < 1:
            flash('First name cannot be blank.', category='error')
        elif len(last_name) < 1:
            flash('Last name cannot be blank.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            # otp_generated=randint(1000,9999)
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'))
            # otp=otp_generated,verified=False)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. Login to continue.',category='success')
            return redirect(url_for('auth.login'))
    
    return render_template("sign_up.html", user=current_user)
