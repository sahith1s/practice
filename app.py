from flask import *
import pandas as pd
import numpy as np
import json
from db.Connection import Connection

import pickle
import os
f = open("C:\\Users\\Sahith\\Desktop\\flask_proj\\ml\\car_api.json")
images = json.load(f)
details = []
model = pickle.load(open(
    "C:\\Users\\Sahith\\Desktop\\flask_proj\\ml\\LinearRegressionModel.pkl", "rb"))
app = Flask(__name__)
# key in server and cookie until and unless seckret_key in server  session valids else session expires
app.secret_key = os.urandom(24)
global conn
# -------------Supporting methods------------


# ---------------------APIs-------------------
car = pd.read_csv(
    'C:\\Users\\Sahith\\Desktop\\flask_proj\\ml\\Cleaned_car.csv')


@app.route('/')
def home():

    return render_template('home.html')


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        mail = request.form.get('email')
        pwdd = request.form.get('pwd')
        rpwdd = request.form.get('rpwd')
        print("........................................................................................")
        print(fname, lname, mail, pwdd, rpwdd)
        query = f"insert into {conn.users_table} values('{fname}','{lname}','{mail}','{pwdd}')"
        print("........................................................................................")
        print(query)
        a = conn.insert(query)
        t = True
        f = False
        if a:
            print("SUCCESS")
            # return redirect(url_for('login_validate'), registration=t)
            return render_template('login.html', registration=t)
        else:
            return render_template('reg.html', registration=f)
    else:
        return render_template('reg.html')


@ app.route('/login', methods=['POST', 'GET'])
def login_validate():
    if request.method == "POST":
        username = request.form.get('uname')
        pwdd = request.form.get('pwd')
        session['username'] = username
        query = f"select * from {conn.users_table} where email='{username}' and pwd='{pwdd}';"
        print(query)
        row = conn.execute(query)
        print(row)
        if row == None:
            return render_template('login.html')
        else:
            # session['fname'] = conn.users_table[0][0]
            return redirect(url_for('main'))
    else:
        if 'username' not in session:
            return render_template('login.html')

        else:
            print("hello")
            return redirect(url_for('main'))


@ app.route('/main')
def main():

    # session['fname'] = conn.users_table[0][0]
    if 'username' in session:
        companies = sorted(car['company'].unique())
        car_models = sorted(car['name'].unique())
        year = sorted(car['year'].unique(), reverse=True)
        fuel_type = car['fuel_type'].unique()
        # if 'fname' in session:
        return render_template('main.html', companies=companies, car_models=car_models, years=year, fuel_type=fuel_type)
    else:
        return redirect(url_for('login_validate'))
        # else:
    #     return redirect(url_for('login_validate'))


@ app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        company = request.form.get('company')
        car_model = request.form.get('car_model')
        year = request.form.get('year')
        fuel_type = request.form.get('fuel_type')
        kms_driven = request.form.get('kilo_driven')
        details = [company, car_model, year, fuel_type, kms_driven]
        print(company, car_model, year, fuel_type, kms_driven)
        prediction = np.round(model.predict(pd.DataFrame([[car_model, company, year, kms_driven, fuel_type]], columns=[
            'name', 'company', 'year', 'kms_driven', 'fuel_type'])), 2)
        print(prediction)
        return render_template('result.html', prediction=prediction, img=images, car_name=car_model, details=details)
    else:
        return render_template('error.html')


@ app.route('/about')
def about():
    return render_template('about.html')


@ app.route('/devloper')
def devloper():
    return render_template('devloper.html')


@ app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')


if __name__ == "__main__":

    # global conn
    conn = Connection()

    app.run(debug=True)
