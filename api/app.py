from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    postGrad = request.form['postGrad']
    nome = request.form['nome']
    ida = request.form['ida']
    volta = request.form['volta']
    destino = request.form['destino']
    
    save_to_database(postGrad, nome, ida, volta, destino)
    return 'Formulário enviado com sucesso!'

@app.route('/relatorios')
def relatorios():
    conn = sqlite3.connect('viagens.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM viagens')
    viagens = cursor.fetchall()
    conn.close()
    return render_template('relatorios.html', viagens=viagens)

@app.route('/dados_viagens')
def dados_viagens():
    conn = sqlite3.connect('viagens.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM viagens')
    viagens = cursor.fetchall()
    conn.close()
    return jsonify(viagens)

@app.route('/delete_viagem', methods=['POST'])
def delete_viagem():
    postGrad = request.form['postGrad']
    nome = request.form['nome']
    ida = request.form['ida']
    volta = request.form['volta']
    destino = request.form['destino']

    conn = sqlite3.connect('viagens.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM viagens WHERE postGrad=? AND nome=? AND ida=? AND volta=? AND destino=?', (postGrad, nome, ida, volta, destino))
    conn.commit()
    conn.close()

    return jsonify({'success': True})


def save_to_database(postGrad, nome, ida, volta, destino):
    conn = sqlite3.connect('viagens.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS viagens (postGrad TEXT, nome TEXT, ida DATE, volta DATE, destino TEXT)')
    cursor.execute('INSERT INTO viagens (postGrad, nome, ida, volta, destino) VALUES (?, ?, ?, ?, ?)', (postGrad, nome, ida, volta, destino))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
