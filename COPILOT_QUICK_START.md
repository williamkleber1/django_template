# GitHub Copilot Quick Start

Este arquivo fornece um resumo rápido das instruções para GitHub Copilot do Django Template.

## 🚀 Setup Rápido

```bash
# 1. Clonar e configurar
git clone https://github.com/williamkleber1/django_template.git
cd django_template

# 2. Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Configurar pre-commit
pre-commit install

# 4. Ambiente local
./dev.sh

# 5. Validar setup
./scripts/validate_instructions.sh
```

## 📚 Documentação Completa

- **[COPILOT_INSTRUCTIONS.md](./COPILOT_INSTRUCTIONS.md)** - Guia completo para desenvolvimento
- **[docs/README.md](./docs/README.md)** - Documentação da API
- **[docs/models.md](./docs/models.md)** - Documentação dos modelos
- **[docs/endpoints.md](./docs/endpoints.md)** - Documentação dos endpoints

## 🧪 Testes (27/27 passando)

```bash
python manage.py test                    # Todos os testes
python manage.py test access            # Testes de autenticação
python manage.py test core              # Testes core
k6 run k6_synthetic_tests.js            # Testes de carga
./test_api_endpoints.sh                 # Testes manuais
```

## 🎨 Qualidade de Código

```bash
black .          # Formatação automática
isort .          # Organizar imports
flake8          # Verificar linting
pre-commit run --all-files  # Executar todos os hooks
```

## 🔄 Workflow de Desenvolvimento

1. **Branch:** `git checkout -b feature/nome-feature`
2. **Código:** Seguir convenções em COPILOT_INSTRUCTIONS.md
3. **Commit:** Pre-commit hooks executam automaticamente
4. **Testes:** `python manage.py test`
5. **Push:** `git push origin feature/nome-feature`

## 📊 Monitoramento

- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin/admin)
- **API Docs:** http://localhost:8000/api/docs/
- **Health:** http://localhost:8000/health/

## 🆘 Problemas Comuns

| Problema | Solução |
|----------|---------|
| Tests failing | `python manage.py test --verbosity=2` |
| Celery not working | Verificar RabbitMQ: `docker-compose ps rabbitmq` |
| Pre-commit failing | `pre-commit run --all-files` |
| Linting errors | `black . && isort . && flake8` |

## 📋 PRs de Referência

- **PR #1:** Template Django base com Celery/RabbitMQ/Observabilidade
- **PR #2:** Sistema de autenticação JWT completo (23 testes)
- **PR #3:** Pre-commit hooks e linting automático
- **PR #4:** Correção de serializers (27 testes passando)
- **PR #5:** Documentação Swagger/OpenAPI completa

## 🎯 Principais Features

- ✅ **Django 5.2** com REST API
- ✅ **JWT Authentication** completo
- ✅ **Celery** para tasks assíncronas
- ✅ **Prometheus/Grafana** para monitoramento
- ✅ **Kubernetes** ready
- ✅ **GitHub Actions** CI/CD
- ✅ **Pre-commit hooks** automáticos
- ✅ **Swagger** documentation
- ✅ **27 testes** unitários + K6 sintéticos