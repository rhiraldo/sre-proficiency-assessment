from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proficiency.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Proficiency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skill = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    evidence = db.Column(db.Text, nullable=True)
    development_plan = db.Column(db.Text, nullable=True)

# Initialize Database
with app.app_context():
    db.create_all()

# Route: Home page
@app.route('/')
def home():
    proficiency_data = Proficiency.query.all()
    return render_template('home.html', proficiency_data=proficiency_data, enumerate=enumerate)

# Route: Add proficiency entry
@app.route('/add', methods=['GET', 'POST'])
def add_proficiency():
    if request.method == 'POST':
        name = request.form['name']
        skill = request.form['skill']
        rating = request.form['rating']
        evidence = request.form['evidence']
        development_plan = request.form['development_plan']

        # Add entry to the database
        new_entry = Proficiency(name=name, skill=skill, rating=rating, evidence=evidence, development_plan=development_plan)
        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html')

# Route: View proficiency details
@app.route('/details/<int:id>')
def details(id):
    entry = Proficiency.query.get_or_404(id)
    return render_template('details.html', entry=entry)

# Route: Delete proficiency entry
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    entry = Proficiency.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)