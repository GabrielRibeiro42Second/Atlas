# Atlas — API de Catálogo Digital

SaaS multi-tenant de catálogo digital para pequenos negócios (barbearias,
restaurantes, lojas de material de construção etc.). Cada empresa gerencia suas
próprias categorias e produtos/serviços via API REST.

**Status:** V1 (REST API) — concluída. Domínio e CRUD de `Company`, `Category`
e `Product` implementados e cobertos por testes.

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

Decisões de exclusão: apagar uma **empresa** remove seus produtos
explicitamente em uma transação e, em seguida, suas categorias e a própria
empresa; a exclusão de uma **categoria que ainda tem produtos** é barrada (`PROTECT`);
produtos podem ser apagados livremente. A relação `Category → Company` usa
`CASCADE`.

## Endpoints

Base: `/api`

| Método | Rota | Ação | Sucesso |
|---|---|---|---|
| GET | `/companies` | lista empresas | `200` |
| POST | `/companies` | cria empresa | `201` |
| GET | `/companies/<pk>` | lê uma empresa | `200` |
| PUT | `/companies/<pk>` | atualiza uma empresa | `200` |
| DELETE | `/companies/<pk>` | apaga uma empresa e seus dados | `204` |
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

# listar empresas
curl http://127.0.0.1:8000/api/companies

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

19 testes de API (TDD — ciclos RED-GREEN-REFACTOR):

```bash
.venv/bin/python manage.py test catalog -v 2
```

Cobertura: CRUD completo de empresas, categorias e produtos, listagens,
cascata de exclusão de empresa, proteção de categoria com produtos, caminhos
de erro (`404`) e criação de categoria duplicada.

## Roadmap

| Versão | Escopo |
|---|---|
| V0 | Domínio (Company, Category, Product) — concluído |
| V1 | REST API + testes — concluído |
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
