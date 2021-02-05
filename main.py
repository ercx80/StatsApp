from flask import Flask, redirect, request, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy

SQLAlchemy_TRACK_MODIFICATIONS=True


app = Flask(__name__)
app.config['SECRET_KEY'] = 'TheSecret'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sql9342668:TKSSHLhfv9@sql9.freemysqlhosting.net/sql9342668'
app.config['SQLALCHEMY_ECHO']= True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Gameplans(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120), unique=True)
    
    forms = db.relationship('Formations', backref='gameplans')

    def __init__(self, name): #this is the database constructor
        self.name=name
        


class Formations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    formation_name= db.Column(db.String(120))
    gameplan_id=db.Column(db.Integer, db.ForeignKey('gameplans.id'))

    variations = db.relationship('Variations', backref='form')
    
    

    def __init__(self, formation_name): #this is the class constructor
        self.formation_name = formation_name
        #self.gameplan = gameplan 


class Variations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    variation_name=db.Column(db.String(120))
    formation_id=db.Column(db.Integer, db.ForeignKey('formations.id'))

    def _init__(self,  variation_name, form):
        self.variation_name= variation_name
        self.form=form

class Totals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direction= db.Column(db.String(120))
    play=db.Column(db.String(120))

    def __init__(self, direction, play):
        self.direction=direction
        self.play = play

@app.route('/')
def index():

   return render_template('index.html')

@app.route('/search', methods=['POST','GET'])
def search():
    return render_template('search.html')

@app.route('/add', methods=['GET','POST'])
def add():
    formations = Formations.query.all()
    variations = Variations.query.all()
    if request.method == 'POST':
        
        plan_name = request.form['plan'] #variable inside the bracket is what the request gets from the form. Name in the template
        new_plan = Gameplans(plan_name) #new_plan is the object created and inside the () is the variable        db.session.add(new_plan)
        session['new_plan'] = new_plan
        db.session.add(new_plan)
        db.session.commit()

        formation_id = int(request.form['formation-id'])
        formations = Formations.query.get(formation_id)
        session['formations'] = formations
        #db.session.add(formation_id)
        #db.session.commit()

        variation_id = int(request.form['variation-id'])
        variations = Variations.query.get(variation_id)
        session['variations'] = variations
        #db.session.add(variation_id)
        #db.session.commit()

        return redirect(url_for('tally'))
    #I need to figure out how to get the name of the objuect but save it on the database
    #as the id 
    

    return render_template('add.html',formations=formations, variations = variations)

@app.route('/tally', methods=['POST','GET'])
def tally():
    new_plan = session['new_plan']
    formations = session['formations']
    variation = session['variations']

    return render_template('tally.html', new_plan=new_plan, formations=formations, variations = variations)
    

        
    
    
    
    





if __name__ == '__main__':
    app.run()

