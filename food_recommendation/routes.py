from food_recommendation import app,db
import json
from flask import render_template,request,redirect,url_for,flash
from food_recommendation.model import User,Records,Orders
from food_recommendation.recommendation import recommend_food
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt()




@app.route("/home",methods=('GET', 'POST'))
@app.route("/",methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        print("hello")
        course_type = request.form['course_type']
        food_type = request.form['food_type']
        dry_or_gravy = request.form['dry_or_gravy']
        print(course_type,food_type,dry_or_gravy)
        with app.app_context():
            db.create_all()
            record=Records(course_type=course_type,food_type=food_type,dry_or_gravy=dry_or_gravy)
            db.session.add(record)
            db.session.commit()
            record=record.to_dict()
            record_id=record['id']
        return redirect(url_for('login',record_id=record_id))

    return render_template('home.html')

def get_total_food():
    with open('food_recommendation/total_food.json') as f:
        food_data = json.load(f)
    return food_data


@app.route("/login", methods=('GET', 'POST'))
def login():
    record_id=request.args.get('record_id')
    if request.method == 'POST':
        error=None
        email = request.form['email']
        password = request.form['password']
        record_id = request.form['record_id']
        user=User.query.filter_by(email=email).all()
        if len(user)==0:
            error=f"The {email} is not registered"
            return render_template('login.html',error=error,record_id=record_id)
        else:
            hash_password=user[0].password
            verify_password=bcrypt.check_password_hash(hash_password,password,record_id=record_id)
            if not verify_password:
                error = "Password not verified"
                return render_template('login.html',error=error,record_id=record_id)
            else:
                query = Records.query.filter_by(id=record_id).all()
                return json.dumps()
                # return redirect(url_for('home'))
            
    return render_template('login.html',record_id=record_id)

@app.route("/signup",methods=('GET','POST'))
def signup():
    print(request.method)
    if request.method == 'POST':
        error=None
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
                error="User already exists"
                return render_template('signup.html',error=error,total_food=get_total_food())
            
            user = User(name=fullname,email=email,password=hashed_password,city=city)
            db.session.add(user)
            db.session.commit()
            user=User.query.all()
            print(user)    
        return redirect(url_for('home'))
    return render_template('signup.html',total_food=get_total_food())

@app.route("/render_signup",methods=('GET','POST'))
def render_signup():
    if request.method == 'POST':
        record_id = request.form['record_id']
        return render_template('signup.html',error=None,record_id=record_id,total_food=get_total_food())

@app.route("/render_login",methods=('GET','POST'))
def render_login():
    if request.method == 'POST':
        record_id = request.form['record_id']
        return render_template('login.html',error=None,record_id=record_id)

if __name__ == '__main__':
    app.run(debug=True)
