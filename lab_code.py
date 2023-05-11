from flask import Flask, render_template, request, url_for, redirect
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import datetime
#4 вариант

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Steps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.Integer, nullable = False)
    date = db.Column(db.Date, nullable = False)


@app.route("/")
def index():
    total = db.session.execute(sqlalchemy.sql.text("SELECT SUM(steps) FROM Steps")).fetchall()[0][0]
    if total == None:
        total = 0
    return render_template('index1.html', records = Steps.query.all(), sum_of_steps = total)

@app.route("/create/", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        steps = request.form['steps']
        date = datetime.datetime.strptime(request.form['date'], "%Y-%m-%d").date()
        stdata = Steps(steps=steps, date=date)
        db.session.add(stdata)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    db.session.execute(sqlalchemy.sql.text("DELETE FROM Steps"))
    db.session.commit()
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()
app.run(debug=True)