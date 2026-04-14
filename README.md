# PROJETO DE RAFAEL E HÉLIO

# 📌 Sistema de Gestão de Rotinas

## 📖 Descrição

Este projeto consiste em uma aplicação backend desenvolvida em Python utilizando Flask, com integração a banco de dados relacional (SQLite).  

O sistema permite o gerenciamento de rotinas pessoais, onde usuários podem criar rotinas, executá-las diariamente e acompanhar o histórico de ações.

---

## 🎯 Objetivo

Permitir que usuários:
- Cadastrem-se no sistema
- Criem rotinas
- Executem rotinas diariamente
- Acompanhem execuções e histórico

---

## 🧱 Estrutura do Banco de Dados

O sistema possui as seguintes tabelas:

### 👤 usuarios
- id (PK)
- nome
- email

---

### 🔁 rotinas
- id (PK)
- nome
- ativa (boolean)
- usuario_id (FK)

Relacionamento:
- Um usuário pode ter várias rotinas (1:N)

---

### 📅 execucoes
- id (PK)
- data
- rotina_id (FK)

Relacionamento:
- Uma rotina pode ter várias execuções (1:N)

---

### 📜 logs
- id (PK)
- acao
- data
- usuario_id (FK)

Relacionamento:
- Um usuário pode ter vários logs (1:N)

---

## ⚙️ Regras de Negócio

- Uma rotina só pode ser executada **uma vez por dia**
- Uma rotina só pode ser executada se estiver **ativa**
- Não é permitido cadastrar usuários com e-mail duplicado
- Todas as ações importantes são registradas em log

---

## 🔗 Rotas da API

### 👤 Usuários
- `POST /usuarios` → Criar usuário
- `GET /usuarios` → Listar usuários

---

### 🔁 Rotinas
- `POST /rotinas` → Criar rotina
- `GET /rotinas` → Listar rotinas
- `PUT /rotinas/{id}` → Atualizar rotina
- `DELETE /rotinas/{id}` → Remover rotina

---

### 📅 Execuções
- `POST /executar` → Executar rotina
- `GET /execucoes` → Listar execuções

---

### 📜 Logs
- `GET /logs` → Listar histórico

---

## 🛠️ Tecnologias Utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Postman

---

## ▶️ Como executar o projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/Rafael-2005/routineManagementSystem.git
cd routineManagementSystem