from food_recommendation import app,db
import json
from flask import render_template,request,redirect,url_for,flash
from food_recommendation.model import User,Records,Orders
from food_recommendation.recommendation import recommend_food,recommend_restaurant
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt()


@app.route("/about")
def about():
    return render_template('about_us.html')

@app.route("/home",methods=('GET', 'POST'))
@app.route("/",methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        print("hello")
        course_type = request.form['course_type']
        food_type = request.form['food_type']
        dry_or_gravy = request.form['dry_or_gravy']
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
            verify_password=bcrypt.check_password_hash(hash_password,password)
            if not verify_password:
                error = "Password not verified"
                return render_template('login.html',error=error,record_id=record_id)
            else:
                print(record_id=='None',type(record_id))
                if record_id=='None':
                    return redirect(url_for('home'))
                record = Records.query.filter_by(id=record_id).first()
                record.user_id=email
                db.session.commit()
                record=record.to_dict()
                orders=Orders.query.filter_by(user_id=email).all()
                orders=[x.to_dict() for x in orders]
                print(orders)
                recom = recommend_food(record['course_type'],record['food_type'],record['dry_or_gravy'],orders)
                return redirect(url_for('recommend_me_food', recom=json.dumps(recom),record_id=record_id))
                # recommend_me_food(recom)

            
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
        confirm_password = request.form['confirm_password']
        if password!=confirm_password:
            error="Pssword you enter are not same."
            return render_template('signup.html',error=error,total_food=get_total_food())
        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        order_list=[['order1','firstdish'],['order2','seconddish'],['order2','thirddish']]
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
            for i in order_list:
                food_choice=request.form[i[1]]
                food_type=request.form[i[0]]
                order= Orders(user_id=email,food_choice=food_choice,food_type=food_type,rating=5)
                db.session.add(order)
                db.session.commit()
            orders=Orders.query.filter_by(user_id=email).all()
            orders=[x.to_dict() for x in orders]
            try:
                record_id = request.form['record_id']
            except:
                return redirect(url_for('home'))
            record = Records.query.filter_by(id=record_id).first()
            record.user_id=email
            db.session.commit()
            record=record.to_dict()
        recom = recommend_food(record['course_type'],record['food_type'],record['dry_or_gravy'],orders)
        return redirect(url_for('recommend_me_food', recom=json.dumps(recom),record_id=record_id))
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

@app.route("/recommend_me_foods",methods=('GET','POST'))
def recommend_me_food():
    if request.method == 'POST':
        max_amount = request.form['max']
        min_amount = request.form['min']
        latitude =request.form['latitude']
        longitude = request.form['longitude']
        suggested_food = request.form['dish']
        record_id = request.form['record_id']
        record = Records.query.filter_by(id=record_id).first()
        record.suggested_food=suggested_food
        print(record.to_dict())
        db.session.commit()
        recom_rest=recommend_restaurant(suggested_food=suggested_food,longitude=longitude,latitude=latitude,min_amount=min_amount,max_amount=max_amount)
        return redirect(url_for('recommend_me_restaurant', recom_rest=json.dumps(recom_rest),record_id=record_id))
    recom=request.args.get('recom')
    record_id=request.args.get('record_id')
    recom=json.loads(recom)
    print(recom,"record_id",record_id)
    return render_template('recommend.html',recom=recom,record_id=record_id)

@app.route("/recommend_me_restaurant",methods=('GET','POST'))
def recommend_me_restaurant():
    recom_rest=request.args.get('recom_rest')
    record_id=request.args.get('record_id')
    recom=json.loads(recom_rest)
    print(recom,"record_id",record_id)
    return render_template('restaurants.html',recom_rest=recom_rest,record_id=record_id)
if __name__ == '__main__':
    app.run(debug=True)
