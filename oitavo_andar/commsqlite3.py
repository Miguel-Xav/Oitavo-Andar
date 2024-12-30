import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

# funções para residências

def criar_tabela_res():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tabela_res(
            id_res INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_res TEXT NOT NULL,
            endereco TEXT NOT NULL,
            cep TEXT NOT NULL,
            morador TEXT
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_res(nome_res, endereco, cep, morador=None):
    conn = get_db_connection()
    cur = conn.cursor()
    nome_mor = morador.nome_mor if morador else None
    cur.execute('INSERT INTO tabela_res (nome_res, endereco, cep, morador) VALUES (?, ?, ?, ?)', (nome_res, endereco, cep, nome_mor))
    conn.commit()
    if morador:
        cur.execute("INSERT INTO tabela_mor (nome_mor, idade, residencia) VALUES (?, ?, ?)",
                    (morador.nome_mor, morador.idade, morador.residencia))
        conn.commit()
    conn.close()
    return id_res

def listar_res():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tabela_res')
    tabela_res = cur.fetchall()
    conn.close()
    return tabela_res

def edit_res(id_res, novo_nome_res, novo_endereco, novo_cep, novo_morador):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tabela_res SET nome_res = ?, endereco = ?, cep = ?, morador = ? WHERE id_res = ?', (novo_nome_res, novo_endereco, novo_cep, novo_morador, id_res))
    conn.commit()
    conn.close()


def checar_residencia(res_id):
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM residencias WHERE id = ?", (res_id,))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado > 0

def deletar_res(id_res):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tabela_res WHERE id_res = ?', (id_res,))
    conn.commit()
    conn.close()

# funções para moradores

def criar_tabela_mor():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tabela_mor(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_mor TEXT NOT NULL,
            idade INTEGER NOT NULL,
            residencia INTEGER NOT NULL,
            FOREIGN KEY(residencia) REFERENCES tabela_res(nome_res)
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_mor(nome_mor, idade, res_mor):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO tabela_mor (nome_mor, idade, residencia) VALUES (?, ?, ?)', (nome_mor, idade, res_mor))
    conn.commit()
    id_mor = cur.lastrowid
    conn.close()
    return id_mor

def listar_mor():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tabela_mor')
    tabela_mor = cur.fetchall()
    conn.close()
    return tabela_mor

def edit_mor(id_mor, novo_nome_mor, nova_idade, novo_residencia):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tabela_mor SET nome_mor = ?, idade = ?, residencia = ? WHERE id = ?', (novo_nome_mor, nova_idade, novo_residencia, id_mor))
    conn.commit()
    conn.close()

def deletar_mor(id_mor):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tabela_mor WHERE id = ?', (id_mor,))
    conn.commit()
    conn.close()

def checar_morador(mor_id):
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM morador WHERE id = ?", (mor_id,))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado > 0