from flask import Flask, redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mybase.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)
app.secret_key = '2Phase'


@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html')


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(50))
    password = db.Column(db.String(50))



@app.route('/singin', methods=['POST', 'GET'])
def singin():
    if request.method == 'POST':
        session.permanent = True
        username = request.form['name']
        password = request.form['password']

        # if len(username) == 0:
        #     flash('Username is empty')
        #     return render_template('singin.html')
        # elif len(password) == 0:
        #     flash('Password is empty')
        #     return render_template('singin.html')
        # elif len(username) <= 3:
        #     flash('Username must be more than 3 character')
        #     return render_template('singin.html')
        # elif len(password) <= 3:
        #     flash('Password must be more than 3 symbol')
        #     return render_template('singin.html')


        if users.query.filter_by(userName=username).first():
            flash('This user already exist!')
            return render_template('singin.html')
        else:
            info = users(userName=username, password=password)
            session.permanent = True
            session['user'] = username
            db.session.add(info)
            db.session.commit()
            flash('Registered Successfully')
            return render_template('weather.html')
    else:
        return render_template('singin.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        username = request.form['name']
        password = request.form['password']
        if users.query.filter_by(userName=username, password=password).first():
            flash('Authorized successfully')
            return render_template('weather.html')
    else:
        return render_template('login.html')


@app.route('/about')
def about():
    return render_template('about.html')




@app.route('/index.html')
def index():
    return render_template('home.html')


@app.route('/weather')
def weather():
    return render_template('weather.html')
    # import requests
    # import json
    # # მომხმარებელს შემოაქ ქალაქის დასახელება. რომელიც უნდა ჩაისეტოს API ლინკში
    # user_city = input("Please enter name of city: ")
    #
    # # ე.წ. API KEy
    # key = '054673ab62682da2ab8c7abd6c098ecf'
    #
    # request_to_api = f'https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={key}'
    #
    # # status code request
    # request_to_server = requests.get(request_to_api)
    # print(request_to_server)
    # print("Status code is: ", request_to_server.status_code)
    #
    # # json file-ის გადაყვანა Dictionary-ში რათა მივწვდეთ Key-ებს.
    #
    # request_to_server_dict = json.loads(request_to_server.text)
    #
    # id = request_to_server_dict['weather'][0]['id']
    # description = request_to_server_dict['weather'][0]['description']
    # print("City id is ", id)
    # if description == 'clear sky' or 'few clouds':
    #     flash('It is Great time for Drift!')
    #     print("City weather Description is ", description)
    # elif description == 'broken clouds':
    #     flash('Maybe it will rain, stay at home!')
    #     print("City weather Description is ", description)
    # else:
    #     flash('stay at home. your health is more important than just a drift! your mother wait at home!')
    #     print("City weather Description is ", description)


if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()
