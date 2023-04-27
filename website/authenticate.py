from flask import Blueprint, render_template, request, redirect, url_for,session
from .models import User
from . import db   #means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import pyrebase,random
authenticate= Blueprint('authenticate', __name__)

firebaseConfig={
  "apiKey": "AIzaSyA7GweUH8Z8Dy_eWJVz2ohpfMaKK-XNTs8",
  "authDomain": "qrbasedordering.firebaseapp.com",
  "databaseURL": "https://qrbasedordering-default-rtdb.firebaseio.com",
  "projectId": "qrbasedordering",
  "storageBucket": "qrbasedordering.appspot.com",
  "messagingSenderId": "364448122744",
  "appId": "1:364448122744:web:476bff4d8e32a9ecc26a8d",
  "measurementId": "G-3HVXNBTYDH"
}
def generate_random_number():
    unique_number = random.randint(100, 999)
    return unique_number
def signup(e,passw):
    firebase=pyrebase.initialize_app(firebaseConfig)
    auth=firebase.auth()
    email=e
    password=passw
    ur=auth.create_user_with_email_and_password(email,password)
  
def loginF(e,passw):
    firebase=pyrebase.initialize_app(firebaseConfig)
    auth=firebase.auth()
    email=e
    password=passw
    try:
        user=auth.sign_in_with_email_and_password(email,password)
        session['user'] = user['idToken']
        return redirect(url_for('authenticate.home'))
    except:
        print("Wrong credentialss")
        return render_template("login2.html")



@authenticate.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            if email=="admin" and password=="admin":
                firebase=pyrebase.initialize_app(firebaseConfig)
                db=firebase.database()
                data = db.child("Orders::").get().val()

                sorted_data = sorted(data.items(), key=lambda x: x[1][0]['Orderid'])

                processed_data = []
                for key, value in sorted_data:
                    processed_data.append({
            'Orderid': value[0]['Orderid'],
            'itemname': value[0]['itemname'],
            'quantity': value[0]['quantity'],
            'Price': value[0]['Price'],
            'Status': value[0]['Status']
            })
                return render_template("admin2.html",data=processed_data)
        
        
            l=loginF(email,password)    
            return l
    return render_template("login2.html")
    


@authenticate.route('/logout')
#@login_required  #checks if user has logged in
def logout():
    session.pop('user', None)
    return redirect(url_for('authenticate.login'))


@authenticate.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        signup(email,password2)
      

    return render_template("login2.html", user=current_user)


@authenticate.route('/')
def home():
    if 'user' in session:
        if 'orderid' not in session:
            no=generate_random_number()
            session['OrderID']=no
        return render_template('home2.html')
    else:
        return redirect(url_for('authenticate.login'))



