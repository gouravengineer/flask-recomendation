from food_recommendation import app,db
from flask import render_template,request,redirect,url_for,flash
from food_recommendation.model import User

@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=('GET', 'POST'))
def login():
    return render_template('login.html')

@app.route("/signup",methods=('GET','POST'))
def signup():
    print(request.method)
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        city =request.form['city']
        password = request.form['password']
        mood = request.form['mood']
        preference = request.form['preference']
        type = request.form['type']
        print(fullname,email,city,password,mood,preference,type)

        # if not name:
        #     flash('Your Full Name is required!')
        # elif not email:
        #     flash('email is required!')
        # elif not password:
        #     flash('Password is required')
            
    return redirect(url_for('home'))

    

if __name__ == '__main__':
    app.run(debug=True)
