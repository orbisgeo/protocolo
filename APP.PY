import sqlite3

# Conectando ao banco de dados
conn = sqlite3.connect('sistema_protocolo.db')
cursor = conn.cursor()

# Apagar a tabela Protocolo, caso já exista
cursor.execute('DROP TABLE IF EXISTS Protocolo')

# Criar a tabela Protocolo
cursor.execute('''
CREATE TABLE Protocolo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    protocolo TEXT,
    data_hora TEXT,
    nome_razao TEXT,
    cpf_cnpj TEXT,
    tipo_licenca TEXT,
    doc_requerente BLOB,
    doc_imovel BLOB,
    projeto BLOB,
    art BLOB
)
''')

# Commit e fechamento da conexão
conn.commit()
conn.close()

print("Tabela 'Protocolo' criada com sucesso!")
