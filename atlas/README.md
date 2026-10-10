# Atlas — API de Catálogo Digital

SaaS multi-tenant de catálogo digital para pequenos negócios (barbearias,
restaurantes, lojas de material de construção etc.). Cada empresa gerencia suas
próprias categorias e produtos/serviços via API REST.

**Status:** V1 (REST API) — em andamento. Domínio e CRUD de `Category` e
`Product` implementados e cobertos por testes.

## Stack

- Python 3.14
- Django 6.1
- Django REST Framework 3.18
- SQLite (hoje) → PostgreSQL + Docker (V2)

## Modelo de domínio

    Company                          raiz do tenant
      │ 1:N   delete → CASCADE
      ▼
    Category (name único por empresa)   UniqueConstraint(company, name)
      │ 1:N   delete com produtos → PROTECT
      ▼
    Product

Decisões de exclusão: apagar uma **empresa** apaga tudo (`CASCADE`); apagar uma
**categoria que ainda tem produtos** é barrada (`PROTECT`); categoria e produto
podem ser apagados livremente (`CASCADE` na cadeia Product → Category → Company).

## Endpoints

Base: `/api`

| Método | Rota | Ação | Sucesso |
|---|---|---|---|
| GET | `/categories` | lista categorias | `200` |
| POST | `/categories` | cria categoria | `201` |
| GET | `/categories/<pk>` | lê uma categoria | `200` |
| PUT | `/categories/<pk>` | atualiza categoria | `200` |
| DELETE | `/categories/<pk>` | apaga categoria | `204` |
| GET | `/products` | lista produtos | `200` |
| POST | `/products` | cria produto | `201` |
| GET | `/products/<pk>` | lê um produto | `200` |
| PUT | `/products/<pk>` | atualiza produto | `200` |
| DELETE | `/products/<pk>` | apaga produto | `204` |

Erros: `400` dados inválidos (ex.: nome duplicado na mesma empresa),
`404` recurso inexistente, `405` verbo não suportado na rota.

### Exemplos

```bash
# criar categoria
curl -X POST http://127.0.0.1:8000/api/categories \
  -H "Content-Type: application/json" \
  -d '{"name": "Cortes", "company": 1}'

# listar produtos
curl http://127.0.0.1:8000/api/products

# apagar categoria
curl -X DELETE http://127.0.0.1:8000/api/categories/1
```

## Setup

Requisitos: Python 3.14+ e [uv](https://docs.astral.sh/uv/).

```bash
git clone <url-do-repositorio>
cd atlas

uv venv .venv
uv pip install django djangorestframework

.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

API disponível em `http://127.0.0.1:8000/api/`.

## Testes

12 testes de API (TDD — ciclos RED-GREEN-REFACTOR):

```bash
.venv/bin/python manage.py test catalog -v 2
```

Cobertura: CRUD completo de categorias e produtos, listagens, caminhos de
erro (`404`) e criação de categoria duplicada.

## Roadmap

| Versão | Escopo |
|---|---|
| V0 | Domínio (Company, Category, Product) — concluído |
| V1 | REST API + testes — em andamento |
| V2 | PostgreSQL + Docker |
| V3 | Autenticação (User, login, autorização) |
| V4 | Multi-tenancy (isolamento de dados entre empresas) |
| V5 | Catálogo público (leitura sem autenticação) |
| V6 | Produção: upload de imagens, busca, paginação, OpenAPI, CI/CD |

## Estrutura

```
atlas/
├── config/        # settings, URLs raiz (project Django)
├── catalog/       # app de negócio: models, serializers, views, urls, tests
├── manage.py
└── README.md
```
