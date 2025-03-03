# Importar Flask y SQLAlchemy
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
name = app
# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creación de la base de datos
db = SQLAlchemy(app)

# Modelo de la tabla Card
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.String(100), nullable=False)


    def _repr_(self):
        return f'<Card {self.id}>'

# Ruta principal para mostrar las tarjetas
@app.route('/')
def index():
    tarjetas = Card.query.all()  # Obtener todas las tarjetas
    return render_template('index.html', tarjetas=tarjetas)

# Ruta para mostrar una tarjeta específica
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get_or_404(id)  # Obtener la tarjeta o mostrar error 404 si no existe opcional
    return render_template('card.html', card=card) # si no quiere el card, debe de quitarlo en esta linea 

# Ruta para mostrar el formulario de creación
@app.route('/create')
def create():
    return render_template('create_card.html')

# Ruta para procesar el formulario de creación
@app.route('/form_create', methods=['POST'])
def form_create():
    title = request.form['title']
    subtitle = request.form['subtitle']
    text = request.form['text']

    nueva_tarjeta = Card(title=title, subtitle=subtitle, text=text)
    db.session.add(nueva_tarjeta)
    db.session.commit()

    return redirect('/')

# Iniciar la aplicación
if __name__ == "_main_":
    with app.app_context():
        db.create_all()  # Crear las tablas si no existen
    app.run(debug=True)