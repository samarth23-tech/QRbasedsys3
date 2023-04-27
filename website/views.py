from flask import Blueprint, render_template,request,redirect,url_for,jsonify,session
#from flask_login import  login_required, current_user
views= Blueprint('views',__name__)
from website import authenticate
import pyrebase
import random



mylist=[]



# Configure Firebase
global config
config = {
  "apiKey": "AIzaSyA7GweUH8Z8Dy_eWJVz2ohpfMaKK-XNTs8",
  "authDomain": "qrbasedordering.firebaseapp.com",
  "databaseURL": "https://qrbasedordering-default-rtdb.firebaseio.com",
  "projectId": "qrbasedordering",
  "storageBucket": "qrbasedordering.appspot.com",
  "messagingSenderId": "364448122744",
  "appId": "1:364448122744:web:476bff4d8e32a9ecc26a8d",
  "measurementId": "G-3HVXNBTYDH"
}

firebase = pyrebase.initialize_app(config)


#creating Order function
# def placeOrder(iname,price,qty):
#     db = firebase.database()
#     title=iname
#     price=price
#     qty=qty
#     orderID = session.get('OrderID')
#     data={"item":title,"price":price,"Quantity":qty,"status":"Waiting"}
#     db.child("Orders:").child(orderID).child("items").set(data)
    
def placeOrder():
    db=firebase.database()
    my_list=session.get('data',[])
    
    db.child("Orders::").child(orderID).set(my_list)

def generate_random_number():
    unique_number = random.randint(100, 999)
    return unique_number



def add_order(iname,price,qty):

    iname=iname
    price=price
    qty=qty
    global orderID
    orderID = session.get('OrderID')
    mylist.append({"Orderid":orderID,"quantity":qty,"Name":title,"Price":price,"Status":"Waiting"})
    session['data']=mylist
    print(mylist)



    
# no=generate_random_number()
#     session['OrderID']=no


@views.route('/dbupd', methods=['POST'])
def update_database():
    tamt = request.form.get('tamt')
    qty=request.form.get('qty')
    itemName=title
    add_order(title,tamt,qty)
    return render_template("payment.html",tamt=tamt)





@views.route("/qrpage")
def index():
    return render_template("index.html")


@views.route("/Order")
def order():
    try:
        placeOrder()
        return "Order placed"
    except:
        return "error"


@views.route("/payment")
#@login_required
def payment():

    return render_template("payment.html")



@views.route("/cart")
def cart_func():
    image=request.args.get('image')
    global title
    title=request.args.get('title')
    price=request.args.get('price')
    no=session['OrderID']
    print(title)
   
    return render_template("newOrder.html",title=title,price=price,no=no)





#FOR ADMIN SIDE



