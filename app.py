"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import os
import os
import pandas as pd
from os.path import join, dirname, realpath
# from werkzeug import secure_filename
# import markdown
# import markdown.extensions.fenced_code
# from pygments.formatters import HtmlFormatter

app = Flask(__name__)
app.secret_key = '1223@#3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.config.from_pyfile('config.cfg')
mail = Mail(app)
s = URLSafeTimedSerializer('Thisisasecret!')
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
class User(db.Model):
    """ Create Data table"""
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(80))
    age = db.Column(db.String(80))
    job = db.Column(db.String(80))
    married = db.Column(db.String(80))
    arrears = db.Column(db.String(80))
    housing = db.Column(db.String(80))
    target = db.Column(db.String(80))
    def __init__(self, town,age, job,married,arrears,housing,target):
        self.town = town
        self.age = age
        self.job = job
        self.married = married
        self.arrears = arrears
        self.housing = housing
        self.target = target 
@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            username = getname(request.form['username'])
            return render_template('index.html', data=getfollowedby(username))
        return render_template('index.html')
@app.route('/upload', methods=['GET', 'POST'])
def upload():
      uploaded_file = request.files['file']
      print(uploaded_file)
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
           # uploaded_file.save(file_path)
           col_names = ['town','age','job', 'married' ,'education' ,'arrears' ,'housing' ,'target']
      # Use Pandas to parse the CSV file
           csvData = pd.read_csv(file_path,names=col_names, header=None)
      # Loop through the Rows
           label=[]
           age=[]
           married=[]
           arrears=[]
           education=[]
           for i,row in csvData.iterrows():

             # new_user = User(
             # town = row['town'],
             # age = row['age'],
             # job = row['job'],
             # married = row['married'],
             # arrears = row['arrears'],
             # housing = row['housing'],
             # target = row['target'])
             # try:
             #  db.session.add(new_user)
             #  db.session.commit()
             # except exc.IntegrityError:
             #  db.session.rollback()
              # return 'Something Wrong'
               label.append(i)
               age.append(row['age']) 
               married.append(row['married']) 
               arrears.append(row['arrears']) 
               education.append(row['education']) 
               print(i,row['town'],row['age'],row['job'],row['married'],row['education'],row['arrears'],
                row['housing'],row['target'])
          # save the file
      return render_template('graph.html',label=label,age=age,married=married,arrears=arrears,education=education)




      # if file and allowed_file(file.filename):
      #       filename = secure_filename(file.filename)
      #       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      #       return f
      #       #return redirect(url_for('uploaded_file',filename=filename))
      #return md_template_string    

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.run(host='0.0.0.0')
    