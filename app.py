from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# CONEXÃO COM O BANCO DE DADOS
CAMINHO_BANCO = os.path.join(app.root_path, 'qualitytrack.db')


def conectar_banco():
    return sqlite3.connect(CAMINHO_BANCO)


# CRIANDO A TABELA
conexao = conectar_banco()

conexao.execute("""
CREATE TABLE IF NOT EXISTS ocorrencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto TEXT NOT NULL,
    defeito TEXT NOT NULL,
    quantidade INTEGER NOT NULL
)
""")

conexao.commit()
conexao.close()


# PÁGINA PRINCIPAL E CADASTRO
@app.route('/', methods=['GET', 'POST'])
def inicio():

    mensagem = ''

    if request.method == 'POST':

        produto = request.form.get('produto', '').strip()
        defeito = request.form.get('defeito', '').strip()
        quantidade = request.form.get('quantidade', '')

        if not produto or not defeito:
            mensagem = 'Preencha todos os campos!'

        else:
            try:
                quantidade = int(quantidade)

                if quantidade <= 0:
                    mensagem = 'A quantidade deve ser maior que zero!'

                else:
                    conexao = conectar_banco()

                    conexao.execute("""
                    INSERT INTO ocorrencias
                    (produto, defeito, quantidade)
                    VALUES (?, ?, ?)
                    """, (produto, defeito, quantidade))

                    conexao.commit()
                    conexao.close()

                    mensagem = 'Ocorrência cadastrada com sucesso!'

            except ValueError:
                mensagem = 'Digite uma quantidade válida!'

    return render_template('index.html', mensagem=mensagem)


# LISTAGEM DE OCORRÊNCIAS
@app.route('/ocorrencias')
def listar_ocorrencias():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT * FROM ocorrencias
    ORDER BY id DESC
    """)

    registros = cursor.fetchall()
    conexao.close()

    return render_template(
        'ocorrencias.html',
        registros=registros
    )


# EDITAR OCORRÊNCIA
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_ocorrencia(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        'SELECT * FROM ocorrencias WHERE id = ?', (id,)
    )

    registro = cursor.fetchone()

    if registro is None:
        conexao.close()
        return 'Ocorrência não encontrada.', 404

    if request.method == 'POST':

        produto = request.form.get('produto', '').strip()
        defeito = request.form.get('defeito', '').strip()
        quantidade_texto = request.form.get('quantidade', '')

        try:
            quantidade = int(quantidade_texto)

            if not produto or not defeito or quantidade <= 0:
                raise ValueError

            cursor.execute("""
            UPDATE ocorrencias
            SET produto = ?, defeito = ?, quantidade = ?
            WHERE id = ?
            """, (produto, defeito, quantidade, id))

            conexao.commit()
            conexao.close()

            return redirect('/ocorrencias')

        except ValueError:

            mensagem = 'Preencha os campos corretamente!'

            registro = (
                registro[0],
                produto,
                defeito,
                quantidade_texto
            )

            conexao.close()

            return render_template(
                'editar.html',
                registro=registro,
                mensagem=mensagem
            )

    conexao.close()

    return render_template(
        'editar.html',
        registro=registro
    )


# EXCLUIR OCORRÊNCIA
@app.route('/excluir/<int:id>', methods=['POST'])
def excluir_ocorrencia(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
    DELETE FROM ocorrencias
    WHERE id = ?
    """, (id,))

    conexao.commit()
    conexao.close()

    return redirect('/ocorrencias')


# DASHBOARD DE INDICADORES
@app.route('/dashboard')
def dashboard():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # TOTAL DE OCORRÊNCIAS
    cursor.execute("""
    SELECT COUNT(*) FROM ocorrencias
    """)

    total_ocorrencias = cursor.fetchone()[0]

    # TOTAL DE PEÇAS AFETADAS
    cursor.execute("""
    SELECT SUM(quantidade) FROM ocorrencias
    """)

    total_pecas = cursor.fetchone()[0] or 0

    # TIPOS DIFERENTES DE DEFEITOS
    cursor.execute("""
    SELECT COUNT(DISTINCT defeito)
    FROM ocorrencias
    """)

    total_tipos = cursor.fetchone()[0]

    # REGISTROS AGRUPADOS POR DEFEITO
    cursor.execute("""
    SELECT defeito, COUNT(*), SUM(quantidade)
    FROM ocorrencias
    GROUP BY defeito
    ORDER BY COUNT(*) DESC
    """)

    defeitos = cursor.fetchall()

    conexao.close()

    defeito_mais_frequente = (
        defeitos[0][0] if defeitos else 'Nenhum'
    )

    return render_template(
        'dashboard.html',
        total_ocorrencias=total_ocorrencias,
        total_pecas=total_pecas,
        total_tipos=total_tipos,
        defeito_mais_frequente=defeito_mais_frequente,
        defeitos=defeitos
    )


if __name__ == '__main__':
    app.run(debug=False)
