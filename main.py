from flask import Flask, redirect, request, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms  import StringField, PasswordField



app = Flask(__name__)
app.config['SECRET_KEY'] = 'TheSecret'
app.config['DEBUG'] = True




@app.route('/', methods=['POST','GET'])
def index():

   return render_template('index.html')

@app.route('/search', methods=['POST','GET'])
def search():
    return render_template('search.html')

@app.route('/add', methods=['POST','GET'])
def add():
    if request.method == 'POST':
        
        plan_name = request.form['name'] #in this line, the variable inside the brakets is the variable passed from the form
        session['plan_name'] = plan_name #Here we store the object plan_name into a session


        formation_name = request.form['formation']
        session['formation_name'] = formation_name
        #formation_names.append(formation_name)

        variation_name = request.form['variation']
        session ['variation_name'] = variation_name
        #variation_names.append(variation_name)
        
        return redirect(url_for('tally'))
    return render_template('add.html')

    
            
            
   

@app.route('/tally', methods=['GET'])
def tally():
    plan_name = session['plan_name']
    formation_name = session['formation_name']
    variation_name = session['variation_name']

    return render_template('tally.html', plan_name=plan_name,formation_name=formation_name,variation_name=variation_name)

@app.route('/results', methods=['GET','POST'])
def results():
    
        counting= int['count1', 'count2']
        for countering in counting:
            countering +=1 
        return ("The total count is ", countering)


    
        


if __name__ == '__main__':
    app.run()

