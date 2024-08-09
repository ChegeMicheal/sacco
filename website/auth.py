from flask import Blueprint, Flask, render_template, request, flash, redirect, url_for,get_flashed_messages
from .models import User,Account,Credit
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import mysql.connector

from flask_mysqldb import MySQL


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('logged in successfully', category= 'success')
                login_user(user, remember=True)
                return redirect(url_for('auth.homepage'))
            else:
                flash('incorrect password, try again', category = 'error')
                
    
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.homepage'))

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fullName = request.form.get('fullname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('email already exists', category = 'error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('password mismatch', category='error')
        elif len(password1) < 7:
            flash('password must be atleast 7 characters.', category='error')
        else:
            #add user to database
            new_user = User(email = email, fullName=fullName, password = generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash('account created successfully!', category='success')
            login_user(user=current_user, remember = True)
            return redirect(url_for('views.homepage'))
        
    return render_template("signUp.html", user = current_user)


@auth.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if request.method == 'POST':
        account_no = request.form.get('account_no')
        account_name = request.form.get('account_name')
        #add account to database
        new_account = Account(account_number=account_no, account_name=account_name)
        db.session.add(new_account)
        db.session.commit()
        flash('account created successfully!', category='success')
        login_user(user=current_user, remember = True)
        return redirect(url_for('auth.homepage'))
        
    return render_template("account.html", user = current_user)

@auth.route('/credits', methods=['GET', 'POST'])  
def credits():
    credits=''
    if request.method == 'POST':
        credit=request.form.get('no_of_credits',type=int)
        for i in range(credit):
            credits+='1'
        #add credits to database
        print(credits)
        new_credit = Credit(credits=credits)
        db.session.add(new_credit)
        db.session.commit()
        flash("REDIRECTING...",'success')
        return redirect(url_for('auth.receipt_cashbook'))
    
    return render_template('credits.html')


@auth.route('/receipt_cashbook', methods=['GET', 'POST'])
def receipt_cashbook():
    def getData():
        mydb = mysql.connector.connect(
             host="d1kb8x1fu8rhcnej.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
             user="mgewt9r4y3xqrzx9",
             passwd="tic4d2e6fe79vw98",
             database="c60lhk7e30osyo5v"
            )
        
        mycursor = mydb.cursor()

        mycursor.execute("select credits from credit ORDER BY id DESC LIMIT 1;") 
        DBData = mycursor.fetchall() 
        print(DBData)
        mycursor.close()
        return DBData
         
    DBData = getData()
    
    return render_template('receipt_cashbook.html',credit=DBData, user=current_user)


@auth.route('/payment_cashbook', methods=['GET', 'POST'])
def payment_cashbook():
    return render_template('payment_cashbook.html', user=current_user)

@auth.route('/petty_cash', methods=['GET', 'POST'])
def petty_cash():
    return render_template('petty_cash.html', user=current_user)

@auth.route('/journal', methods=['GET', 'POST'])
def journal():
    return render_template('journal.html', user=current_user)


@auth.route('/updateProfile', methods=['GET', 'POST'])
def updateProfile():
    
    return render_template('updateProfile.html', user=current_user)

@auth.route('/loan', methods=['GET', 'POST'])
def loan():
    return render_template('loan.html', user=current_user)

@auth.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    user = User.query.all()
    return render_template('home.html', user=current_user)

@auth.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html', user=current_user)

app= Flask(__name__)
app.config["IMAGE_UPLOADS"]= r'C:\Users\USER\Desktop\sacco\website\static\images\uploads'
app.config["ALLOWED_IMAGE_EXTENSIONS"]=["PNG","JPG","JPEG","GIF"]
app.config["MAX_IMAGE_FILESIZE"]=0.5 * 1024 * 1024


def allowed_image(filename):
    if not '.' in filename:
        return False
    
    ext = filename.rsplit('.',1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False
    




@auth.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if request.files:
            
            image=request.files["image"]

            if image.filename == "":
                print("image must have a filename")
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                print("that image extension is not allowed")
                return redirect(request.url)
            
            else:
                filename=secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"],filename))
                flash('image uploaded successfully!')
                print("image saved!")
            
            return redirect(request.url)
    
            

    return render_template('upload_image.html', user=current_user)


@auth.route('/send_messages', methods=['GET', 'POST'])
def send_messages():
    if request.method == 'POST':
        email = request.form.get('email')
        message = request.form.get('message')
        visibility = request.form.get('visibility')
        #add user to database
        new_message = Footer_message(email = email, message=message, visibility=visibility)
        db.session.add(new_message)
        db.session.commit()
        flash('message submitted!', category='success')
        
    return render_template("homepage.html")
    


@auth.route('/view_messages', methods=['GET', 'POST'])
def view_messages():
    
    def getData():
        mydb = mysql.connector.connect(
             host="d1kb8x1fu8rhcnej.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
             user="mgewt9r4y3xqrzx9",
             passwd="tic4d2e6fe79vw98",
             database="c60lhk7e30osyo5v"
            )
        
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM footer_message WHERE visibility='public'") 
        DBData = mycursor.fetchall() 
        print(DBData)
        mycursor.close()
        return DBData
         
    DBData = getData()
    return render_template("messages.html", footer_message=DBData)

@auth.route('/view_private_messages', methods=['GET', 'POST'])
def view_private_messages():
    
    def getData():
        mydb = mysql.connector.connect(
             host="d1kb8x1fu8rhcnej.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
             user="mgewt9r4y3xqrzx9",
             passwd="tic4d2e6fe79vw98",
             database="c60lhk7e30osyo5v"
            )
        
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM footer_message WHERE visibility='private'") 
        DBData = mycursor.fetchall() 
        print(DBData)
        mycursor.close()
        return DBData
         
    DBData = getData()
    return render_template("private_messages.html", footer_message=DBData)

    #footer_message = Footer_message.query.all()
    #print(footer_message)
    #return render_template('messages.html', footer_message=footer_message)


#create custom error pages

#invalid url
@auth.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

#internal server error
@auth.errorhandler(500)
def server_error(e):
    return render_template("500.html"),500