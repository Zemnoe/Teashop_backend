from flask import Flask, render_template

app = Flask (__name__)


@app.route ('/')
def index():
    return render_template ('index.html')

@app.route ('/login')
def login():
    return render_template('login.post')
    
@app.route ('/registration') 
def registration():
    return render_template('registration.html')

@app.route ('/order')
def order():
    return render_template('order.html')

if __name__ == '_main_':
   app.run(debug=True)



    