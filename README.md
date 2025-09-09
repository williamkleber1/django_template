# Django Template com Celery, RabbitMQ e Observabilidade

Esta é uma aplicação Django completa com integração de Celery para processamento de tarefas assíncronas, RabbitMQ como message broker, observabilidade com Grafana/Prometheus, e deployment com Kubernetes e GitHub Actions.

## Características

- **Django 5.2** - Framework web principal
- **Celery** - Processamento de tarefas distribuídas
- **RabbitMQ** - Message broker para Celery
- **Redis** - Backend de resultados para Celery
- **PostgreSQL** - Banco de dados principal
- **Prometheus** - Coleta de métricas
- **Grafana** - Visualização de métricas e dashboards
- **Docker** - Containerização
- **Kubernetes** - Orquestração de containers
- **GitHub Actions** - CI/CD pipeline

## Estrutura do Projeto

```
.
├── django_app/          # Configurações principais do Django
├── core/                # App principal com views e tasks
├── k8s/                 # Manifestos Kubernetes
├── monitoring/          # Configurações Prometheus/Grafana
├── .github/workflows/   # GitHub Actions
├── docker-compose.yml   # Ambiente local
├── Dockerfile          # Imagem Django
├── Dockerfile.celery   # Imagem Celery
└── requirements.txt    # Dependências Python
```

## Desenvolvimento Local

### Pré-requisitos
- Docker e Docker Compose
- Python 3.12+

### Executar localmente

1. Clone o repositório
2. Execute com Docker Compose:

```bash
docker-compose up --build
```

Serviços disponíveis:
- **Django App**: http://localhost:8000
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)

### APIs Disponíveis

- `GET /` - Home page com informações da API
- `GET /health/` - Health check
- `POST /tasks/` - Criar tarefas Celery
- `GET /tasks/<task_id>/` - Status da tarefa
- `GET /metrics` - Métricas Prometheus

### Exemplo de uso das APIs

```bash
# Criar tarefa de adição
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"type": "add", "x": 5, "y": 3}'

# Criar tarefa longa
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"type": "long_running", "duration": 10}'

# Verificar status da tarefa
curl http://localhost:8000/tasks/<task_id>/
```

## Deploy em Kubernetes

### Pré-requisitos
- Cluster Kubernetes
- kubectl configurado

### Deploy

```bash
# Aplicar todos os manifestos
kubectl apply -f k8s/

# Verificar deployments
kubectl get pods -n django-app
kubectl get services -n django-app
```

### Acesso aos serviços

```bash
# Port forward para desenvolvimento
kubectl port-forward -n django-app service/django-service 8000:80
kubectl port-forward -n django-app service/grafana-service 3000:3000
kubectl port-forward -n django-app service/prometheus-service 9090:9090
```

## CI/CD Pipeline

O pipeline GitHub Actions inclui:

1. **Test** - Testes unitários com serviços PostgreSQL, Redis e RabbitMQ
2. **Build** - Build e push das imagens Docker para GitHub Container Registry
3. **Deploy** - Deploy automático para Kubernetes (configuração necessária)

### Configuração necessária

Para o deploy automático funcionar, configure:

1. **Secrets do GitHub**:
   - `KUBECONFIG` - Configuração do cluster Kubernetes

2. **Permissões**:
   - Package write permissions para GitHub Container Registry

## Observabilidade

### Métricas Disponíveis

- HTTP requests e response times
- Database connections
- Celery task metrics
- Sistema metrics (CPU, memória)

### Dashboards Grafana

O projeto inclui dashboard pré-configurado com:
- Taxa de requisições HTTP
- Tempo de resposta
- Status codes HTTP
- Conexões de banco de dados

## Configurações de Ambiente

Principais variáveis de ambiente:

```bash
# Django
SECRET_KEY=sua-chave-secreta
DEBUG=false
ALLOWED_HOSTS=localhost,seu-dominio.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=django_app
DB_USER=postgres
DB_PASSWORD=senha
DB_HOST=postgres-service
DB_PORT=5432

# Celery
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq-service:5672//
CELERY_RESULT_BACKEND=redis://redis-service:6379/0
```

## Desenvolvimento

### Adicionar novas tarefas Celery

1. Edite `core/tasks.py`
2. Adicione nova view em `core/views.py`
3. Atualize as rotas em `core/urls.py`

### Customizar métricas

1. Edite as configurações em `django_app/settings.py`
2. Atualize `monitoring/prometheus.yml`
3. Modifique dashboards em `monitoring/grafana/dashboards/`

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.
