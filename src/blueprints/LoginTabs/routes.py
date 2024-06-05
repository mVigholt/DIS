from flask import render_template, url_for, redirect, request, Blueprint , jsonify
from flask_login import login_user, current_user, logout_user
import os
import pandas

from src.forms import ManagerLoginForm, UserSignupForm
from src.models import Manager, Customer
from src.queries import get_user_by_user_name, insert_manager, insert_customer
from src.utils.choices import ClubChoices
from src import app

Login = Blueprint('Login', __name__)


@Login.route("/")
@Login.route("/home")
def home():
    return render_template('pages/home.html')


@Login.route("/about")
def about():
    return render_template('pages/about.html')


@Login.route("/style-guide")
def style_guide():
    return render_template('pages/style-guide.html')


@Login.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))
    form = ManagerLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = get_user_by_user_name(form.user_name.data)
            if user and user['password'] == form.password.data:
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('Login.home'))
    return render_template('pages/login.html', form=form)


@Login.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))
    form = UserSignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_data = dict(full_name=form.full_name.data,
                             user_name=form.user_name.data,
                             password=form.password.data)
            
            manager = Manager(user_data)
            insert_manager(manager)
           
            user = get_user_by_user_name(form.user_name.data)
            if user:
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('Login.home'))
    return render_template('pages/signup.html', form=form)





@Login.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Login.login'))

