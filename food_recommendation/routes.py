from food_recommendation import app
from flask import render_template

@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=('GET', 'POST'))
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)