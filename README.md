Biblioteca Online — Django + DRF

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.16-red?style=for-the-badge&logo=django)](https://www.django-rest-framework.org/)

Aplicação web e API REST para uma biblioteca online. Os usuários podem se cadastrar, fazer login, pesquisar livros na OpenLibrary e registrar aluguéis com data de entrega. A API expõe endpoints para gerenciar usuários e os aluguéis do usuário autenticado (via sessão).

---

## ✨ Funcionalidades Principais

- API REST: CRUD de `Usuarios` e `Livros` (aluguéis).
- Busca externa: integração com a API pública da OpenLibrary para pesquisar títulos.
- Sessão de usuário: login simples (armazenado em `request.session`).
- Interface Web: páginas para login, cadastro, pesquisa de livros e "Meus aluguéis".
- Segurança básica: senhas de usuários são salvas com hash (Django).

---

## 🛠 Tecnologias Utilizadas

- Backend:
  - Python
  - Django 5.2.x
  - Django REST Framework 3.16.x
- Banco de Dados:
  - SQLite3 (padrão do projeto)
- Requisições Externas:
  - Requests (OpenLibrary)
- Frontend:
  - HTML5 + CSS (Django Templates)

---

## 🚀 Como Rodar o Projeto

### 1) Pré-requisitos

- Python 3.11 ou superior
- Git

### 2) Clonar o Repositório

```
git clone https://github.com/leonardolucasbs/wsBackend-Fabrica25.2.git .
cd <PASTA_DO_REPO>
```

### 3) Criar e Ativar o Ambiente Virtual

```
python -m venv venv

# Windows
./venv/Scripts/activate
# Linux / macOS
source venv/bin/activate
```

### 4) Instalar Dependências

```
pip install -r requirements.txt
```

### 5) Migrar o Banco de Dados
````
python manage.py makemigrations
````

```
python manage.py migrate
```

### 6) Executar o Servidor

```
python manage.py runserver
```

Acesse a aplicação em: http://localhost:8000/

---

## 🌐 Rotas e Endpoints

Base do projeto: `http://localhost:8000/`

### Interface Web (Templates)

- `http://127.0.0.1:8000` : página de Login.
- `/cadastro/`: página de Cadastro.
- `/home/`: pesquisa de livros (OpenLibrary) e ação de aluguel.
- `/alugar/`: confirmação de aluguel e escolha da data de entrega.
- `/locacoes/`: listagem de aluguéis do usuário logado.
- `/logout/`: encerra a sessão do usuário.

Observação: a busca usa `https://openlibrary.org/search.json?q=<termo>&page=<n>` e exibe capas via `covers.openlibrary.org` quando disponíveis.

### API REST (DRF)

Base da API: `http://localhost:8000/api/`

- `GET /usuarios/`: lista usuários.
- `POST /usuarios/`: cria usuário. Exemplo payload:
  ```json
  { "nome": "Maria", "email": "maria@exemplo.com", "senha": "segredo123" }
  ```
- `GET /usuarios/{id}/`: detalhes.
- `PUT/PATCH /usuarios/{id}/`: atualiza.
- `DELETE /usuarios/{id}/`: remove.

- `GET /livros/`: lista aluguéis do usuário da sessão atual.
- `POST /livros/`: cria aluguel para o usuário da sessão. Exemplo payload:
  ```json
    {"usuario": 3,  "titulo": "Introdução ao COBOL",  "autor": "Grace Hopper",  "data_entrega": "2025-09-30"}

  ```
- `GET /livros/{id}/`: detalhes.
- `PUT/PATCH /livros/{id}/`: atualiza.
- `DELETE /livros/{id}/`: remove.

Importante: os endpoints de `livros` usam a sessão (`request.session["usuario_id"]`). Para consumir a API de `livros` fora do navegador, primeiro autentique pelo formulário web para obter o cookie de sessão.

---

## 🧱 Modelos (Resumo)

- `Usuarios`: `id`, `nome`, `email` (único), `senha` (hash).
- `Livros`: `id`, `usuario` (FK), `titulo`, `autor`, `data_aluguel` (auto), `data_entrega`.

---

## 🧪 Dicas de Desenvolvimento

- Admin (`/admin/`): disponível, porém os modelos não estão registrados por padrão.
- Idioma e fuso: `pt-br` e `America/Recife` configurados em `project/settings.py`.
- DRF: `rest_framework` já adicionado ao projeto.

---

## 📌 Roadmap Sugerido

- Registrar modelos no admin para inspeção rápida.
- Proteções adicionais para API (permissões e autenticação).
- Validação de datas de entrega no backend/API.
- Paginação e filtros na listagem de aluguéis.


