from functools import wraps
from flask.json import JSONEncoder
from flask_mysqldb import MySQL

from flask_mail import Mail, Message
from wtforms import SelectField
from selenium import webdriver

import re, random, requests, time, redis, os, codecs, urllib.request, json
import selenium.webdriver.chrome.service as service
from flask import Flask,render_template,flash,request,redirect, url_for, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators 
import json as json
from gtts import gTTS #converts speech to text - google API

myapp = Flask(__name__)
#MySQL configuration code
myapp.config['MYSQL_HOST']='localhost'
myapp.config['MYSQL_USER']='root'
myapp.config['MYSQL_PASSWORD']=''
myapp.config['MYSQL_DB']='SMARTHOMEdB'
myapp.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(myapp)

#MAIL SERVER-SETUP (YAHOO.MAIL)
myapp.config.update(dict(
Mail_SERVER='smtp.mail.yahoo.com',
MAIL_PORT=465,
MAIL_USE_SSL=True,
MAIL_USERNAME='alexapetrei7@yahoo.com',
MAIL_PASSWORD='finalyear2019'))
mail=Mail(myapp)


myapp.debug=True
@myapp.route('/')
def index():
    return render_template('index.html')
def talk(text):
    tts=gTTS(text, lang='en')
#talk defined as text-the speech transforms to text

#user register form
class UserRegister(Form):
    userName =StringField('User Name',
    [validators.Length(min=1,max=50),
    validators.DataRequired()])
    email=StringField('Email',[
    validators.Length(min=6,max=100),
    validators.DataRequired()])
    password =PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Password are not the same')
    ])
    confirm=PasswordField('Confirm your Password')

#method get / post 
@myapp.route('/Register', methods=['GET','POST'])

def user_Register():
    form =UserRegister(request.form)
    if request.method=='POST' and form.validate(): #colecct user-data from the form- see below
        userName=form.userName.data
        email=form.email.data
        password=(form.password.data)

        query=mysql.connection.cursor()
        query.execute("INSERT INTO user(userName,email,password) VALUES(%s, %s, %s)",(userName,email,password))
    
 #adds users to the database
      
        mysql.connection.commit()
#terminate connection
       
        query.close()
 #close the connection
        
        flash("You have now Successfuly Registered with SmartHomeApp, Please LogIn!",'pass')
        return redirect(url_for('login'))
       

    return render_template('Register.html',form=form)

@myapp.route('/login', methods=['GET','POST'])

def login():
    if request.method=='POST':
        username=request.form['email'] #use email in username field to log in
        formPASSword=request.form['password']  #password passed through the form
        query=mysql.connection.cursor()

        fetch=query.execute("SELECT * FROM user WHERE email=%s",[username])

        if fetch>0: #if there is any user here
            data=query.fetchone()#will determine if there is a use what could happen
            password=data['password'] #password obtained form db
           
            if (formPASSword,password): #check if the passwords are the same
                session['loggedin']=True
                session['userName']=data['userName']
                flash('You have Logged In Successfuly','pass')
                text="Welcome To Smart Home,  I am you Home App Assistant"
                talk(text)
                return redirect(url_for('control'))


            else:
                text="Invalid Username and or Password"

                flash("Invalid username and or password",'fail')
                talk(text)

                return render_template('login.html')
            #close connection
            query.close()

        else:
            errors='There is NO user Logged In'
            return render_template('login.html',errors=errors)


    return render_template('login.html')


# will check if the user is logged in before loading other pages
def mandatory_login(f):
    @wraps(f)
    def check_loggedin(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            text=("You have to Login To Control the App")
            #say("Incorrect username and password")
            talk(text)
            flash('You have to Login To Control the App', 'fail')
            return redirect(url_for('login', next=request.url))
    return check_loggedin

#methods Post / Get to send requests 
@myapp.route('/control', methods=['POST','GET'])
@mandatory_login
def control():

    if request.method=="POST":
      
        userRequest=request.form['userrInput']
        if userRequest=='BedRoom-LIGHT-ON':
            deviceId=540
            newState=1
            deviceName='BedroomLight'
            deviceLoc='BedRoom'
         
            rand=random.random()
            verifySt = checkState(deviceId,newState,deviceName,deviceLoc)

        elif userRequest=='BedRoom-LIGHT-OFF':
            deviceId=540
            newState=0
            deviceName='BedroomLight'
            deviceLoc='BedROOM'
         
            rand=random.random()
            verifySt = checkState(deviceId,newState,deviceName,deviceLoc)
        elif userRequest=='Corridor-LIGHT-ON':
            deviceId=547
            newState=1
            deviceName='CorridorLight'
            deviceLoc='Corridor'
      
            rand=random.random()
            verifySt = checkState(deviceId,newState,deviceName,deviceLoc)
        elif userRequest=='Corridor-LIGHT-OFF':
            deviceId=547
            newState=0
            deviceName='CorridorLight'
            deviceLoc='Corridor'

            rand=random.random()
            verifySt = checkState(deviceId,newState,deviceName,deviceLoc)
        elif userRequest=='Kettle-ON':
            deviceId=19
            newState=1
            deviceName='Kettle'
            deviceLoc='Kitchen'
           
            rand=random.random()
            verifySt = checkState(deviceId,newState,deviceName,deviceLoc)
        elif userRequest=='Kettle-OFF':
            deviceId=19
            newState=0
            deviceName='Kettle'
            deviceLoc='Kitchen'
            
            rand=random.random()
            verifySt = checkState(deviceId,newState,deviceName,deviceLoc)
        elif userRequest=='LivingRoom-LAMP-OFF':
            deviceId =39
            newState=0
            deviceName='[L]BigLamp'
            deviceLoc='LivingRoom'
            rand=random.random()
            
            verifySt = checkState(ddeviceIdevId,newState,deviceName,deviceLoc)
        elif userRequest=='LivingRoom-LAMP-ON':
            deviceId =39
            newState=1
            deviceName='[L]BigLamp'
            deviceLoc='LivingRoom'
           
            rand=random.random()
            verifySt = checkState(deviceId,newState,deviceName,deviceLoc)

    
        else:
            return 'There is no Request Recieved'
        if verifySt:
            return verifySt
    return render_template('control.html')

#check  device current state
def checkState(deviceId,newState,deviceName,deviceLoc):

    rand=random.random()
    respond=urllib.request.urlopen("http://10.12.102.156:3480/data_request?id=status&output_format=json&DeviceNum=%s"%(deviceId))
    str_respond=respond.read().decode('utf-8')
    states=json.loads(str_respond)['Device_Num_'+str(deviceId)]['states']

    for state in states:
        if state["variable"] == "Status":
            deviceState = state["value"]
            if deviceState == str(newState):
                text="device is on the same state as you requested"
                flash("Sorry, Device is on the same state as you requested",'danger')
                talk(text)
                return render_template('control.html')
       
#this function changes the device state
def load():

    return redirect(url_for('control'))


def devState(deviceId,newState,rand):
    try:
        respond = "http://10.12.102.156/port_3480/data_request?id=lu_action&output_format=json&DeviceNum=%s&serviceId=urn" \
        ":upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=%s&rand=%s "%(deviceId,newState,rand)
        urllib.request.urlopen(respond)
        text="Changing the device state"
        talk(text)
        reload = load()
      
    except:
        flash('errors')
    if reload:
        return reload
    return render_template('control.html')

#logout
@myapp.route('/log_out')
def log_out():
    session.clear()
    flash('You are Logged Out','success')
    text="You are Logged Out"
    talk(text)
    return redirect(url_for('index'))



if __name__=='__main__':

    myapp.secret_key='final2019' # protection/your app will not work without a secretkey
    myapp.run(host='127.0.0.1',port=8000) #host and port running - host is database ip
