from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "semana_santa_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False, unique=True)

    def __init__(self, city, number):
        self.city = city
        self.number = number

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        number = request.form['number']

        # Verificar si el número ya existe para la ciudad seleccionada
        existing_card = Card.query.filter_by(city=city, number=number).first()
        if existing_card:
            flash('Carta repetida', 'error')
        else:
            new_card = Card(city=city, number=number)
            db.session.add(new_card)
            db.session.commit()
            flash('Carta guardada con éxito', 'success')

    return render_template('index.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
