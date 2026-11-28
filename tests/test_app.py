
import pytest
import app as qualitytrack


# Preparação do banco para cada teste
@pytest.fixture
def banco():
    with qualitytrack.conectar_banco() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                TRUNCATE TABLE ocorrencias
                RESTART IDENTITY
            """)

    yield

    # Limpa os dados depois do teste
    with qualitytrack.conectar_banco() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                TRUNCATE TABLE ocorrencias
                RESTART IDENTITY
            """)


# Cliente de testes do Flask
@pytest.fixture
def client(banco):
    qualitytrack.app.config['TESTING'] = True

    with qualitytrack.app.test_client() as cliente:
        yield cliente


# TESTE 1: Página inicial
def test_pagina_inicial(client):
    resposta = client.get('/')

    assert resposta.status_code == 200


# TESTE 2: Cadastro de ocorrência
def test_cadastrar_ocorrencia(client):
    resposta = client.post('/', data={
        'produto': 'Espelho',
        'defeito': 'Risco',
        'quantidade': '5'
    })

    assert resposta.status_code == 200

    with qualitytrack.conectar_banco() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                SELECT produto, defeito, quantidade
                FROM ocorrencias
            """)

            registro = cursor.fetchone()

    assert registro == ('Espelho', 'Risco', 5)
