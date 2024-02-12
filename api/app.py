from flask import Flask, render_template, request, jsonify
from models import Viagens, db, create_tables

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://default:kaDLqePyI4b9@ep-crimson-poetry-a4wbybo0.us-east-1.aws.neon.tech:5432/verceldb' # não pode ficar diretamente no código, falha de segurança gravissima
db.init_app(app)

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    nova_viagem = Viagens(
        postGrad=request.form['postGrad'],
        nome=request.form['nome'],
        ida=request.form['ida'],
        volta=request.form['volta'],
        destino=request.form['destino']
    )
    db.session.add(nova_viagem)
    db.session.commit()
    return 'Formulário enviado com sucesso!'

@app.route('/relatorios')
def relatorios():
    viagens = Viagens.query.all()
    return render_template('relatorios.html', viagens=viagens)

@app.route('/dados_viagens')
def dados_viagens():
    viagens = Viagens.query.all()
    return jsonify([{
        'postGrad': viagem.postGrad,
        'nome': viagem.nome,
        'ida': viagem.ida,
        'volta': viagem.volta,
        'destino': viagem.destino
    } for viagem in viagens])

@app.route('/delete_viagem', methods=['POST'])
def delete_viagem():
    postGrad = request.form['postGrad']
    nome = request.form['nome']
    ida = request.form['ida']
    volta = request.form['volta']
    destino = request.form['destino']
    viagem = Viagens.query.filter_by(postGrad=postGrad, nome=nome, ida=ida, volta=volta, destino=destino).first() # isso é má pratica o ideal é trafegar apenas 1 id unico
    if viagem:
        db.session.delete(viagem)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Viagem não encontrada'})

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Rota não encontrada'}), 404

with app.app_context():
    create_tables()

if __name__ == '__main__':
    app.run(debug=True)
