from fileinput import filename
import os
from tokenize import group
from app import app, db
from load_model import predict
from models import User,Record
from flask import render_template, request, redirect, url_for, flash,session


basedir = os.path.abspath(os.path.dirname(__file__))


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'super_user' in session:
        return redirect(url_for('dashboard'))
    if request.method == "POST":
        id = request.form.get('ID')
        password = request.form.get('Password')

        if id == 'super_admin' and password == '#admin':
            session['super_user']="super_user"
            return redirect(url_for('dashboard'))
        else:
            user = User.query.get(id)
            print(user.soinik_number)
            if user==None or user.password!=password:
                return render_template('login.html',msg='userId and password do not match')
            else:
                session['user']=user.soinik_number
                return redirect(url_for('user_dashboard'))
    else:
        return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'super_user' in session:
        users = User.query.all()
        print(users)
        return render_template('dashboard.html',users=users,length = len(users))
    else:
        return redirect(url_for('login'))

@app.route('/user_dashboard')
def user_dashboard():
    if 'user' in session:
        users = User.query.get(session['user'])
        return render_template('user_dashboard.html',users=[users],length = len([users]))
    else: redirect(url_for('login'))


@app.route('/add_new_entry', methods=['GET', 'POST'])
def add_new_entry():
    if 'super_user' in session:
        if request.method == "POST":
            soinik_number = request.form.get('soinik_number')
            rank = request.form.get('rank')
            name = request.form.get('name')
            company = request.form.get('company')

            print(soinik_number,rank,name,company)
            if soinik_number.isdigit():
                new_user = User(soinik_number,rank,name,company)
                check = User.query.get(soinik_number)

                if check!=None:
                    return render_template('add_new_entry.html', msg="soinik number already exist")
                
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    return render_template('add_new_entry.html', msg="new entry has been added successfully")
                except:
                    return render_template('add_new_entry.html', msg="Oops failed to add the new entry")
            else:
                return render_template('add_new_entry.html', msg="soinik number must be an integer")
          
        else:

            return render_template('add_new_entry.html')
    else:
        return redirect(url_for('login'))


@app.route('/upload_image',methods=['GET', 'POST'])
def upload_image():
    if 'super_user' in session:
        if request.method == "POST":
            soinik_number = request.form.get('soinik_number')
            date = request.form.get('date')
            image = request.files['file']
            dir_path = 'static/uploads/'
            dir_path =  os.path.join(dir_path,soinik_number+'/'+date+'/')
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            count = len(os.listdir(dir_path))
            image_path = os.path.join(dir_path,str(count+1)+'-'+image.filename)
            image.save(image_path)
            file_name = str(count+1)+'-'+image.filename
            new_record = Record(soinik_number,date.replace('-','/'),count+1,file_name)
            db.session.add(new_record)
            db.session.commit()
            return render_template('upload_image.html', msg = "image uploaded successfully")
        else:
            return render_template('upload_image.html')
    else:
        return redirect(url_for('login'))


@app.route('/show_record')
def show_record():
    if 'super_user' in session:
        records = Record.query.all()
        print(records)
        return render_template('show_record.html',ln= len(records),records=records)
    else:
        return redirect(url_for('login'))

@app.route('/display_image/<soinik_number>/<date>/<file_name>')
def display_image(soinik_number,date,file_name):
    print(soinik_number,date,file_name)
    return redirect(url_for('static',filename='uploads/'+soinik_number+'/'+date+'/'+file_name),code=301)


@app.route('/calculate_grouping')
def calculate_grouping():
    if 'super_user' in session:
        return render_template('calculate_grouping.html')
    else:
        return redirect(url_for('login'))


@app.route('/analysis_error',methods = ["GET","POST"])
def analysis_error():
    if 'super_user' in session:
        if request.method == "POST":
            soinik_number = request.form.get('soinik_number')
            date = request.form.get('date')
            sub_label = request.form.get('sub_label')
            print(date)
            record = Record.query.filter_by(soinik_number=soinik_number,date=date.replace('-','/'),sub_label=sub_label).all()
            
            print(record)
            # grouping = request.form.get('grouping')
            error = predict('static/uploads/'+soinik_number+'/'+date+'/'+ record[0].file_name)
            print(error)
            record[0].error = error
            record[0].total_hit = 5
            db.session.add(record[0])
            db.session.commit()
            return render_template('analysis_error.html')
        else:
            return render_template('analysis_error.html')
    else:
        return redirect(url_for('login'))


@app.route('/report')
def report():
    if 'super_user' in session:
        users = User.query.all()
        print(users)
        return render_template('report.html',users=users,length = len(users))
    else:
        return redirect(url_for('login'))


@app.route('/show_report')
def show_report():
    if 'super_user' in session:
        records = Record.query.all()
        return render_template('show_report.html',ln= len(records),records=records)
    else:
        return redirect(url_for('login'))


@app.route('/signout')
def signout():
    session.pop('super_user',None)
    session.pop('user',None)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Page not Found<h1>'


if __name__ == "__main__":
    app.run(debug=True)
