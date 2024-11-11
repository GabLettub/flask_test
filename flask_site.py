from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model): # initializess the model table
    idNum = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

with app.app_context(): 
    db.create_all() # creates the table

@app.route("/")
def index():
    items = Item.query.all() #eq to SQL: select * 
    return render_template('index.html', items=items)


#CRUD: simple view configs /3
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        new_item = Item(name=name)
        db.session.add(new_item)
        db.session.commit() #finalizes 
        return redirect(url_for('index')) #redirects the view of the user towards 'index'
    return render_template('create.html')

@app.route('/update/<int:idNum>', methods=['GET', 'POST'])
def update(idNum):
    item = Item.query.get_or_404(idNum) #find idNum if none, yield 404 page
    if request.method == 'POST':
        item.name = request.form['name']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/delete/<int:idNum>', methods=['POST'])
def delete(idNum):
    item = Item.query.get_or_404(idNum)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/hello")
@app.route("/hello/")
@app.route("/hello/<user_name>")

def hello(user_name=None):
    return render_template('home.html', user=user_name)
