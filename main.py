from flask import Flask, redirect, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

SQLAlchemy_TRACK_MODIFICATIONS=True


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sql9342668:TKSSHLhfv9@sql9.freemysqlhosting.net/sql9342668'
app.config['SQLALCHEMY_ECHO']= True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Gameplans(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120))
    
    forms = db.relationship('Formations', backref='gameplan')

    def __init__(self, name):
        self.name=name
        


class Formations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    formation= db.Column(db.String(120))
    gameplan_id=db.Column(db.Integer, db.ForeignKey('gameplans.id'))

    variations = db.relationship('Variations', backref='form')
    
    

    def __init__(self, formation, gameplan): #this is the class constructor
        self.formation = formation
        self.gameplan = gameplan 


class Variations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    variation=db.Column(db.String(120))
    formation_id=db.Column(db.Integer, db.ForeignKey('formations.id'))

    def _init__(self,  variations, form):
        self.variations= variations
        self.form=form

class Totals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direction= db.Column(db.String(120))
    play=db.Column(db.String(120))

    def __init__(self, direction, play):
        self.direction=direction
        self.play = play

@app.route('/', methods=['POST','GET'])
def index():

   return render_template('index.html')

@app.route('/search', methods=['POST','GET'])
def search():
    return render_template('search.html')

@app.route('/add', methods=['POST','GET'])
def add():
    plan_name = ''
    formation_choice = ''
    variation_choice = ''


    plan_error = ''
    formation_error = ''
    variation_error = ''

    if request.method == 'POST':
        plan_name = request.form['plan']
        formation_choice = request.form['choice']
        variation_choice = request.form['variation']
        
        if plan_name == '':
            plan_error = 'This field cannot be empty'
        if formation_choice == '':
            formation_error = 'Please choose a formation'
        if variation_choice == '':
            variation_error = 'Please choose a variation'
        
        if not plan_error and not formation_error and not variation_error:
            new_plan = Gameplans(plan_name)
            new_form = Formations(formation_choice)
            new_var = Variations(variation_choice)

            db.session.add(new_plan, new_form, new_var)
            db.session.commit()
            return redirect('/tally?id={}'.format(new_plan.id, new_form.id, new_var.id))
        else:
                return render_template('add.html', plan_error, formation_error, variation_error)
            
    return render_template('add.html')

@app.route('/tally', methods=['POST','GET'])
def tally():
    return render_template('tally.html')





if __name__ == '__main__':
    app.run()

