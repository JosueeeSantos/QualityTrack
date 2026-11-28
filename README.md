# QualityTrack — Sistema de Gestão da Qualidade

Sistema web desenvolvido em Python e Flask para registrar, consultar, editar e excluir ocorrências de qualidade, além de acompanhar indicadores por meio de um dashboard.

O projeto foi desenvolvido com o objetivo de aplicar conhecimentos de programação, desenvolvimento web, banco de dados e automação de testes em uma aplicação prática.

**Acesse a aplicação:** [QualityTrack — Aplicação online](https://qualitytrack-gzqv.onrender.com)

## Funcionalidades

- **Cadastro de ocorrências:** registro de produtos, defeitos e quantidades afetadas.
- **Consulta de ocorrências:** visualização dos registros cadastrados.
- **Edição de registros:** atualização das informações das ocorrências.
- **Exclusão de registros:** remoção de ocorrências cadastradas.
- **Dashboard de indicadores:** acompanhamento do total de ocorrências, peças afetadas e tipos de defeitos.
- **Análise de defeitos:** identificação dos defeitos mais frequentes.
- **Persistência de dados:** armazenamento das informações em PostgreSQL.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| Flask | Desenvolvimento da aplicação web |
| PostgreSQL | Banco de dados relacional |
| Neon | Banco PostgreSQL em nuvem |
| HTML5 | Estrutura das páginas |
| CSS3 | Estilização da interface |
| Pytest | Testes automatizados |
| GitHub Actions | Automação dos testes |
| Render | Hospedagem da aplicação |

## Como executar localmente

### 1. Clone o repositório

Clone o projeto pelo GitHub e entre na pasta `QualityTrack`.

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

Ative o ambiente virtual:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Configure a variável de ambiente `DATABASE_URL` com a URL de conexão de um banco PostgreSQL.

**Windows PowerShell:**
```powershell
$env:DATABASE_URL="sua_url_de_conexao_postgresql"
```

**Linux/macOS:**
```bash
export DATABASE_URL="sua_url_de_conexao_postgresql"
```

Não compartilhe sua URL de conexão nem publique credenciais no repositório.

### 5. Execute a aplicação

```bash
python app.py
```

Acesse no navegador:

```text
http://127.0.0.1:5000
```

## Testes automatizados

O projeto utiliza Pytest para verificar o funcionamento das principais funcionalidades.

Para executar os testes:

```bash
python -m pytest -v
```

O GitHub Actions executa automaticamente os testes a cada atualização da branch `main` e em Pull Requests.

Os testes automatizados utilizam um banco PostgreSQL temporário, separado do banco de produção.

**Importante:** ao executar os testes localmente, utilize um banco exclusivo para testes, pois a preparação dos testes limpa os registros da tabela `ocorrencias`.

## Hospedagem

A aplicação está publicada na plataforma Render e utiliza PostgreSQL hospedado no Neon para persistência dos dados.

- Aplicação: https://qualitytrack-gzqv.onrender.com
- Hospedagem: Render
- Banco de dados: Neon PostgreSQL

## Objetivo do projeto

O QualityTrack representa a aplicação prática de conhecimentos em desenvolvimento de software, integração com banco de dados, criação de interfaces web, testes automatizados e publicação de aplicações.

O projeto continua em evolução, com foco no aprimoramento das funcionalidades e na qualidade do código.

---

**Desenvolvido como projeto de portfólio em Ciência da Computação.**
