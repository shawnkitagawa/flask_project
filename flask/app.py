from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from config import * 
import pandas as pd
import re
from datetime import date
from datetime import datetime , timedelta
import time
import datetime
import calendar
import json
import jyserver.Flask as jsf
API_KEY = api_key_id
SECRET_KEY = secret_key


from flask import Flask, render_template, url_for, request, redirect, session, flash
# from login import login
from flask_sqlalchemy import SQLAlchemy
import os
import flask


app = Flask(__name__)
app.secret_key = "ShawnKitagawaProgrammer"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.permanent_session_lifetime = timedelta(hours = 5)



# @jsf.use(app)

# class App:
#     def __init__(self):
#         self.ticker_price = 128
#     def ticker(self):
#         self.ticker_price += 1
#         self.js.document.getElementById("current_price").innerHTML = self.ticker_price



# app.register_blueprint(login, url_prefix="/login_page")
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer, primary_key = True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email






@app.context_processor   
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
            print(values)
    return url_for(endpoint, **values)


    

@app.route("/", methods =['POST','GET'])
def index():
    return render_template("index2.html")

@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())


@app.route('/StockAnalysis', methods =['POST','GET'])
def stock():
    ticker = ""
    if flask.request.method == 'POST':
        print(request.args)
        print(request.data)
        print(request.json)
        print(request.values)
        # text = request.args.get('Ticker')
        text = request.json.get("Ticker")

        print(text)
    else:
        text = "failed"
    print(text)
    # Get the current price
    stock_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
    ticker = text

    # Get todays date
    #Check if the stock market is close or not, if its close it will give an error since
    # openning does not exist in that day 
    # closes weekends and holidays 

    #check if today is a holiday
    holiday = False
    closed = False
    price_reason = ""
    week_num = date.today().weekday()
    print(week_num)
    dates = date.today()
    current_time = time.ctime()
    current_time = time.strftime("%H:%M:%S")
    print(current_time)



    
    # HOLIDAY                                                                                                                           
    if (dates.strftime("%m-%d") == "01-17") or (dates.strftime("%m-%d") == "02-21") or (dates.strftime("%m-%d") == "04-15") or (dates.strftime("%m-%d") == "05-30") or (dates.strftime("%m-%d") == "06-19") or (dates.strftime("%m-%d") == "07-04") or (dates.strftime("%m-%d") == "09-05") or (dates.strftime("%m-%d") == "11-24") or (dates.strftime("%m-%d") == "12-25"):
        holiday = True
        closed = True
        if (week_num == 6):
            dates = datetime.datetime.today()-datetime.timedelta(days=2)
            price_reason = "Due to holidays"
        elif (week_num == 5):
            dates = datetime.datetime.today()-datetime.timedelta(days=1)
            price_reason = "Due to holidays"
            


    # If the holiday is on Sunday and observed on Monday 
    if week_num == 0:
        if (((datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%m-%d") == "01-17") or ((datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%m-%d") == "01-17") or ((datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%m-%d") == "02-21") or ((datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%m-%d") == "04-15") or ((datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%m-%d") == "05-30") or ((datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%m-%d") == "06-19") or ((datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%m-%d") == "07-04") or ((datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%m-%d") == "09-05") or ((datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%m-%d") == "11-24") or ((datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%m-%d") == "12-25")):
            dates = datetime.datetime.today()-datetime.timedelta(days=3)
            holiday = True
            closed = True
            price_reason = "due to holiday on Sunday, observed today"
    # If the holiday is on Saturday and observed on Friday
    if week_num == 4:
        if (((datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%m-%d") == "01-17") or ((datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%m-%d") == "01-17") or ((datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%m-%d") == "02-21") or ((datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%m-%d") == "04-15") or ((datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%m-%d") == "05-30") or ((datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%m-%d") == "06-19") or ((datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%m-%d") == "07-04") or ((datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%m-%d") == "09-05") or ((datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%m-%d") == "11-24") or ((datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%m-%d") == "12-25")):
            dates = datetime.datetime.today()-datetime.timedelta(days=1)
            holiday = True
            closed = True
            price_reason = "due to holiday on Saturday, observed today"

    if (week_num > 4) and (holiday == False):
        if week_num == 5:
            dates = datetime.datetime.today()-datetime.timedelta(days=1)
            closed = True
            price_reason = "Weekends closing"

        elif week_num == 6:
            dates = datetime.datetime.today()-datetime.timedelta(days=2)
            closed = True
            price_reason = "Weekends closing"
    # get rid of time just the year-month and the day
    dates = dates.strftime("%Y-%m-%d")
    print(dates)



    
    #Get the current price
    count = 0
    error = False
    while True:
        count += 1
        try:
            if ticker == "failed":
                ticker = "AAPL"

            requests_params = StockBarsRequest(
            timeframe =TimeFrame.Day,
            symbol_or_symbols=[ticker],
            start =pd.Timestamp(f"{dates}")
            #end = pd.Timestamp("2022-09-30")
            )

            bars = stock_client.get_stock_bars(requests_params)

            stock_info = bars[ticker][0]
            print(stock_info)
            break
        except:
            print("The market is close right now")
            dates = datetime.datetime.today()-datetime.timedelta(days= count)
            dates = dates.strftime("%Y-%m-%d")
            closed = True
            if (count == 4):
                print("the price does not exist in Alpaca API")
                error = True
                break




    #Get open price if its weekdays or non holiday
    # get closing price of the last market price if the market is close
    # Need to display if its a opening price of the date or closing -----------------------------------
    count = 0
    if error == True:
        current_price = 0000000
        price_status = "This ticker does not exist in the Alpaca API "
        price_reason = "error occured"
    else:


        price_status = ""
        for i in stock_info:
            if closed == False:
                if count == 2:
                    current_price = i[1]
                    price_status = "Open Price"
                
            elif closed:
                if count == 5:
                    current_price = i[1]
                    price_status = "Closing Price"
            
            count+=1
        print(current_price)
        print("the name of the ticker is ")
        print(ticker)
        data = {"ticker": ticker, "current_price": current_price}
        return render_template("index.html",data = data, current_price = current_price, ticker = ticker, price = price_status, date = dates, price_reason = price_reason)
        

        



    # return render_template('index.html', current_price = current_price, ticker = ticker, price = price_status, date = dates, price_reason = price_reason )
    return render_template("index.html",current_price = current_price, ticker = ticker, price = price_status, date = dates, price_reason = price_reason)



@app.route("/login" ,methods =["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"] 
        user = request.form["nm"]
        session["user"] = user
        session["email"] = email
        flash("You are succesfully logged in")

        found_user = users.query.filter_by(email = email).first()

        if found_user == None:
            usr = users(user,email)
            db.session.add(usr)
            db.session.commit()
        return redirect(url_for("user"))
    else:
        if ("user" in session) and ("email" in session):
            return redirect(url_for("user"))
    return render_template("login.html")


@app.route("/user")
def user():
    if ("user" in session) and ("email" in session):
        user = session["user"]
        email = session["email"]
        return render_template("user.html", user = user, email = email)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if ("user" in session) and ("email" in session):
        flash("You have been logged out!", "info")
        session.pop("user",None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)