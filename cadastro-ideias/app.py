from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ideas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Adicione uma chave secreta para flash messages

db = SQLAlchemy(app)

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    message = request.args.get('message')
    category = request.args.get('category')
    return render_template('index.html', message=message, category=category)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        topic = request.form['topic']
        description = request.form['description']
        summary = request.form['summary']
        author = request.form['author']

        new_idea = Idea(topic=topic, description=description, summary=summary, author=author)
        db.session.add(new_idea)
        db.session.commit()
        return redirect(url_for('index', message='Ideia cadastrada com sucesso!', category='success'))
    except Exception as e:
        return redirect(url_for('index', message='Erro ao cadastrar a ideia. Tente novamente.', category='danger'))

@app.route('/view')
def view():
    ideas = Idea.query.all()
    return render_template('view.html', ideas=ideas)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    idea = Idea.query.get_or_404(id)
    if request.method == 'POST':
        idea.topic = request.form['topic']
        idea.description = request.form['description']
        idea.summary = request.form['summary']
        idea.author = request.form['author']
        db.session.commit()
        return redirect(url_for('view'))
    return render_template('edit.html', idea=idea)

if __name__ == "__main__":
    app.run()
