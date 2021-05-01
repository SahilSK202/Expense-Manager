from flask import Flask , render_template , request , redirect
app = Flask(__name__)
# app means website in flask

# Creating class for database WITH SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime ,timezone
import pytz

IST = pytz.timezone('Asia/Kolkata')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Expense.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Expense(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    memo = db.Column(db.String(200), nullable = False)
    inward = db.Column(db.Float, nullable = False)
    outward = db.Column(db.Float, nullable = False )
    date_created = db.Column(db.DateTime,  default = datetime.strptime(datetime.now(IST).strftime('%d/%m/%y %I:%M %S'),('%d/%m/%y %I:%M %S')))

# This method return string when object of a class is called alone
    def __repr__(self) -> str:
        '''This method return string when object of a class is called alone
'''
        return f"{self.sno},{self.memo},{self.inward},{self.outward}"


# open python with terminal
# from app import db
# db.create_all()
# This will create database
# go to sqlite viewer on chrome

@app.route('/' , methods = ['GET' , 'POST'])
# just to return a text
# def hello():
#     return 'Hello World !'  

# To return html 
def rend():
    if request.method == 'POST':
        memo = request.form['memo']
        amount = request.form['amount']
        entrytype = request.form['type']
        # print("entrytype :",entrytype)
        if(entrytype == "Inward"):
            inward = amount
            outward = 0
        else:
            outward = amount
            inward = 0
        Exp_obj = Expense(memo = memo , inward = inward , outward = outward , date_created = datetime.strptime(datetime.now(IST).strftime('%d/%m/%y %I:%M %S'),('%d/%m/%y %I:%M %S')) )
        db.session.add(Exp_obj)
        db.session.commit()
    allexp = Expense.query.all()
    # print(alltodo) # uses repr function
    # return render_template('index.html')
    return render_template('index.html' , allexp = allexp)

# Boostrap has readymade templates getbootstrap.com
# jinja2 is a template used for passing python variables to html
    
@app.route('/show')
def products():
    allexp = Expense.query.all()
    print(allexp) # uses repr function
    return 'Hello , Explore your list !'
    
@app.route('/update/<int:sno>' ,methods = ['GET' , 'POST'])
def update(sno):
    if request.method == 'POST':
        memo = request.form['memo']
        inward = request.form['inward']
        outward = request.form['outward']
        toupdate = Expense.query.filter_by(sno = sno).first()
        toupdate.memo = memo
        toupdate.inward = inward
        toupdate.outward = outward
        db.session.add(toupdate)
        db.session.commit()
        return redirect("/")

    toupdate = Expense.query.filter_by(sno = sno).first()
    # db.session.delete(toupdate)
    # db.session.commit()
    # print(alltodo) # uses repr function
    return render_template('update.html' , toupdate = toupdate )
    
@app.route('/delete/<int:sno>')
def delete(sno):
    todelete = Expense.query.filter_by(sno = sno).first()
    db.session.delete(todelete)
    db.session.commit()
    print(todelete) # uses repr function
    return redirect("/")

# Create static and templates directories
# static/sahil.txt to render files statically
# templates/index.html to render templates

if __name__ == "__main__":
    app.run(debug = True)