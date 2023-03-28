from food_recommendation import app,db
from flask import render_template,request,redirect,url_for,flash
from food_recommendation.model import User
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt()

@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'Post':
        error=None
        email = request.form['email']
        password = request.form['password']
        user=User.query.filter_by(email=email).all()
        if len(user)==0:
            error=f"The {email} is not registered"
            return render_template('login.html',error=error)
        else:
            hash_password=user[0].password
            verify_password=bcrypt.check_password_hash(hash_password,password)
            if not verify_password:
                error = "Password not verified"
                return render_template('login.html',error=error)
            else:
                return redirect(url_for('home'))
            
    return render_template('login.html')

@app.route("/signup",methods=('GET','POST'))
def signup():
    print(request.method)
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        city =request.form['city']
        password = request.form['password']
        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        mood = request.form['mood']
        preference = request.form['preference']
        type = request.form['type']
        with app.app_context():
            db.create_all()
            check = User.query.filter_by(email=email).all()
            print(check)
            if len(check)!=0:
                flash("User already Existed")
                # return redirect(url_for('sig'))
            
            user = User(name=fullname,email=email,password=hashed_password,city=city)
            db.session.add(user)
            db.session.commit()
            user=User.query.all()
            print(user)
            
    return redirect(url_for('home'))

    

if __name__ == '__main__':
    app.run(debug=True)
