from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuração do diretório de upload
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função para conectar ao banco de dados e criá-lo se não existir
def get_db_connection():
    db_path = 'sistema_protocolo.db'
    
    # Se o banco não existir, cria a estrutura inicial
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Protocolo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                protocolo TEXT,
                data_hora TEXT,
                nome_razao TEXT,
                cpf_cnpj TEXT,
                tipo_licenca TEXT,
                doc_requerente TEXT,
                doc_imovel TEXT,
                projeto TEXT,
                art TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Protocolo")
    protocolos = cursor.fetchall()
    conn.close()
    return render_template('index.html', protocolos=protocolos)

@app.route('/add', methods=['POST'])
def add_protocolo():
    protocolo = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    nome_razao = request.form['nome_razao']
    cpf_cnpj = request.form['cpf_cnpj']
    tipo_licenca = request.form['tipo_licenca']

    doc_requerente_path = salvar_arquivo(request.files.get('doc_requerente'), protocolo)
    doc_imovel_path = salvar_arquivo(request.files.get('doc_imovel'), protocolo)
    projeto_path = salvar_arquivo(request.files.get('projeto'), protocolo)
    art_path = salvar_arquivo(request.files.get('art'), protocolo)

    conn = get_db_connection()
    conn.execute('''
    INSERT INTO Protocolo (protocolo, data_hora, nome_razao, cpf_cnpj, tipo_licenca, doc_requerente, doc_imovel, projeto, art)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (protocolo, data_hora, nome_razao, cpf_cnpj, tipo_licenca, doc_requerente_path, doc_imovel_path, projeto_path, art_path))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

def salvar_arquivo(arquivo, protocolo):
    if arquivo and arquivo.filename:
        filename = secure_filename(f"{protocolo}_{arquivo.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        arquivo.save(filepath)
        return filename  # Salva apenas o nome do arquivo no banco de dados
    return None

# Rota para download do arquivo
@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Verifique se o arquivo existe antes de servir
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return "Arquivo não encontrado", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


