from flask import render_template, request, redirect, url_for, session, flash
from wtforms import ValidationError,StringField, PasswordField, validators
from flask_login import login_user
from app.home import home
from app import mongo, bcrypt, login_manager
from app.home.user_loging_manager import User
from flask import request, redirect
from werkzeug.utils import secure_filename
import os,shutil
import hashlib
import phonenumbers
from flask_wtf import Form
from wtforms.fields.html5 import DateField
from app.home.RegisterForm import RegisterForm
from bs4 import BeautifulSoup
import re
from dateutil.relativedelta import *
from datetime import date, datetime
import requests




APP_ROOT = os.path.dirname(os.path.abspath(__file__))



def calculate_age(born_date):
    today = date.today()
    split_date = born_date.split('/')
    dob = date(int(split_date[2]), int(split_date[1]), int(split_date[0]))
    age = relativedelta(today, dob)
    return age.years


def parser():
    try:
        url="https://news.google.com/covid19/map?hl=en-IN&mid=/m/03rk0&gl=IN&ceid=IN:en"
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
    except:
        url = "/data/interview/dezzex/flask-registration-master/app/home/corona_data.html"
        page = open(url)
        soup = BeautifulSoup(page.read())

    
    cities = soup.find_all('tr', {'class' : 'sgXwHf wdLSAe YvL7re'})
    try:    
        table_html = str(soup.find_all('table', {'class':'pH8O4c'})[0]).replace('class="pH8O4c"', 'class="pH8O4c" style="width:100%"').replace('Sorted by Confirmed in descending order','')
    except:
        table_html = None
    return table_html

def PasswordCreate(user_in):
    password1 = hashlib.md5()
    password1.update(user_in.encode("utf-8"))
    return password1.hexdigest()


@login_manager.user_loader
def load_user(email):
    users = mongo.db.users.find_one({'email': email})
    if not users:
        return None
    return User(users['email'])


@home.route('/')
def start():
    return render_template('index.html')



@home.route('/sign', methods=['POST', 'GET'])
def sign():
    if request.method == 'POST':
        email = request.form['inputEmail']
        user_name = request.form['inputUserName']
        password = request.form['inputPassword']
        corona_table = parser()
        

        user = mongo.db.users.find_one({'email': email})
        if user:
            if User.validate_login(user['password'], password):
                image_location = mongo.db.users.find_one({'email': email})['image'].split('/')[-1]
                session['user-email']=email
                session['user-name']=user_name
                session['table-data']=corona_table
                session['user-image']=image_location
                user_obj = User(email)
                login_user(user_obj)
                return redirect(url_for('user.profile'))
            else:
                print('Incorrect Credentials')
        else:
            return redirect(url_for('home.register'))
    return render_template('home/sign.html')



@home.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_md5 = PasswordCreate(password)
        inputFullName = request.form['full_name']
        inputDOB = request.form['dob']
        inputPassport = request.form['passport']
        inputPhone = request.form['phone_number']
        inputUserName = request.form['username']
        ageField = calculate_age(inputDOB)


        target = os.path.join(APP_ROOT, 'user-images')  #folder path
        if not os.path.isdir(target):
                os.mkdir(target)     # create folder if not exits

        filename = secure_filename(form.image_file.data.filename)
        destination = "/".join([target, filename])
        form.image_file.data.save(destination)


        if mongo.db.users.find_one({'email': email}):
            return redirect(url_for('home.sign'))
        else:
            mongo.db.users.insert({'email': email, 'password': password_md5, 'age':ageField, 'full_name':inputFullName, 'DOB':inputDOB, 'passport_number':inputPassport, 'phone_number':inputPhone, 'user_name':inputUserName, 'image':destination})
            return redirect(url_for('home.sign'))

    return render_template('home/register.html', form = form)