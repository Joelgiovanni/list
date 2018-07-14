from flask import Flask, redirect, render_template,request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/joelgodoy/Desktop/FLASK/list1/database.db'

db = SQLAlchemy(app)


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    incomplete = List.query.filter_by(complete=False).all()
    complete = List.query.filter_by(complete=True).all()

    return render_template('index.html', complete=complete, incomplete=incomplete)

@app.route('/add', methods=['POST'])
def add():
    list = List(text=request.form['newitem'], complete=False)
    db.session.add(list)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):
    list = List.query.filter_by(id=int(id)).first()
    list.complete = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/incomplete/<id>')
def incomplete(id):
    list = List.query.filter_by(id=int(id)).first()
    list.complete = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    List.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)