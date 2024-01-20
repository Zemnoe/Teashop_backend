from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, text
from models.models import *
import hashlib

app = Flask(__name__)
app.secret_key="greatness"
app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://root:Cogistics1/@localhost/teashop_data'
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

Base.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST'and 'email' in request.form and 'password' in request.form:

    
        email = request.form['email']
        password = request.form['password']

        
        hash = password + app.secret_key
        hash = hashlib.sha256(hash.encode())
        password = hash.hexdigest()

        
        with engine.connect() as con:
            result = con.execute(text(f"Select * from user where email = '{email}' and password = '{password}'"))
            account = result.fetchone()
            con.commit()

        if account:
            session['loggedin'] = True
            session['id'] = account.id
            session['email'] = account.email
            msg = "Logged in successfully"
            return redirect(url_for('dashboard', msg=msg))
        else:
            msg = "Incorrect email/password"
    return render_template('login.html', msg=msg)   
       


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg =""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        #get the form values
        username = request.form['username'].lower()
        email = request.form['email']
        password = request.form['password']
       
        with engine.connect() as con:
            result = con.execute(text(f"Select * from user where username = '{username}'"))
            account = result.fetchone()
            con.commit()
        if account:
            msg = "Account already exists"
            return render_template('register.html', msg=msg)
        
        if not username or not password or not email:
                msg = "Please fill out the form"
                return render_template('register.html', msg=msg)
        else:
            
            hash = password + app.secret_key
            hash = hashlib.sha256(hash.encode())
            password = hash.hexdigest()
            #insert the user into the database
            with engine.connect() as con:
                con.execute(text(f"Insert into user (username, password, email) values ('{username}', '{password}', '{email}')"))
                con.commit()
            msg = "Account created successfully"
            return redirect(url_for('login', msg=msg))
    return render_template('register.html', msg=msg)


@app.route('/order')
def order():
    return render_template('order.html')
    

if __name__ == '__main__':
    app.run(debug=True)