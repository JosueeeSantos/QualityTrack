import sqlite3
import app as qualitytrack


def criar_banco(caminho):
    conexao = sqlite3.connect(caminho)

    conexao.execute("""
        CREATE TABLE ocorrencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            defeito TEXT NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def test_pagina_inicial(client):
    resposta = client.get('/')

    assert resposta.status_code == 200


def test_cadastrar_ocorrencia(client, banco):
    resposta = client.post('/', data={
        'produto': 'Espelho',
        'defeito': 'Risco',
        'quantidade': '5'
    })

    assert resposta.status_code == 200

    conexao = sqlite3.connect(banco)
    registro = conexao.execute(
        "SELECT produto, defeito, quantidade FROM ocorrencias"
    ).fetchone()
    conexao.close()

    assert registro == ('Espelho', 'Risco', 5)


# Preparação do ambiente de testes
import pytest


@pytest.fixture
def banco(tmp_path, monkeypatch):
    caminho = tmp_path / 'teste.db'

    criar_banco(caminho)

    monkeypatch.setattr(
        qualitytrack,
        'CAMINHO_BANCO',
        str(caminho)
    )

    return str(caminho)


@pytest.fixture
def client(banco):
    qualitytrack.app.config['TESTING'] = True

    with qualitytrack.app.test_client() as cliente:
        yield cliente
