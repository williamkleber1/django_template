# Django Template - GitHub Copilot Instructions

Este documento fornece instruções detalhadas para desenvolvimento com GitHub Copilot neste template Django completo com Celery, RabbitMQ e observabilidade.

## 📋 Índice

- [Visão Geral do Projeto](#visão-geral-do-projeto)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Histórico de Desenvolvimento (PRs)](#histórico-de-desenvolvimento-prs)
- [Fluxo de Desenvolvimento](#fluxo-de-desenvolvimento)
- [Convenções de Código](#convenções-de-código)
- [Testes e Qualidade](#testes-e-qualidade)
- [Monitoramento e Logs](#monitoramento-e-logs)
- [Deployment e CI/CD](#deployment-e-cicd)
- [Exemplos de Desenvolvimento](#exemplos-de-desenvolvimento)
- [Troubleshooting](#troubleshooting)

## 🎯 Visão Geral do Projeto

Este é um template Django 5.2 completo para aplicações de produção com:

### Tecnologias Principais
- **Django 5.2** - Framework web principal
- **Celery 5.5.3** - Processamento de tarefas distribuídas
- **RabbitMQ** - Message broker para Celery
- **Redis 5.2.1** - Backend de resultados para Celery
- **PostgreSQL** - Banco de dados principal
- **Django REST Framework 3.15.2** - API REST
- **JWT Authentication** - Sistema de autenticação

### Observabilidade e Monitoramento
- **Prometheus** - Coleta de métricas
- **Grafana** - Visualização de métricas e dashboards
- **django-prometheus** - Middleware de métricas
- **Logging estruturado** - Para debugging e monitoramento

### DevOps e Qualidade
- **Docker & docker-compose** - Containerização
- **Kubernetes** - Orquestração de containers
- **GitHub Actions** - CI/CD pipeline
- **Pre-commit hooks** - Qualidade de código
- **Black, flake8, isort** - Linting e formatação

## 📁 Estrutura do Projeto

```
django_template/
├── django_app/              # Configurações principais do Django
│   ├── settings.py          # Configurações centrais
│   ├── urls.py              # URLs principais
│   ├── celery.py            # Configuração do Celery
│   └── wsgi.py              # WSGI application
├── access/                  # App de autenticação e usuários
│   ├── models.py            # CustomUserModel e models relacionados
│   ├── serializers.py       # Serializers DRF
│   ├── views.py             # ViewSets de API
│   ├── urls.py              # URLs da API de acesso
│   └── tests.py             # 23+ testes unitários
├── core/                    # App principal com views e tasks
│   ├── views.py             # Endpoints principais (health, tasks)
│   ├── tasks.py             # Tarefas Celery
│   ├── urls.py              # URLs core
│   └── tests.py             # Testes das funcionalidades core
├── general/                 # App base com abstrações
│   ├── models.py            # BaseModel abstrato
│   └── utils.py             # Utilities gerais
├── docs/                    # Documentação técnica
│   ├── README.md            # API overview
│   ├── models.md            # Documentação dos models
│   ├── endpoints.md         # Documentação dos endpoints
│   └── test_documentation.py # Testes da documentação
├── k8s/                     # Manifestos Kubernetes
│   ├── namespace.yaml       # Namespace django-app
│   ├── django-deployment.yaml # Deployment Django
│   ├── celery-deployment.yaml # Deployment Celery
│   ├── postgres-deployment.yaml # PostgreSQL
│   ├── redis-deployment.yaml   # Redis
│   ├── rabbitmq-deployment.yaml # RabbitMQ
│   └── monitoring/          # Prometheus e Grafana
├── monitoring/              # Configurações de monitoramento
│   ├── prometheus.yml       # Configuração Prometheus
│   └── grafana/            # Dashboards Grafana
├── .github/workflows/       # GitHub Actions
│   └── ci-cd.yml           # Pipeline CI/CD
├── scripts/                 # Scripts utilitários
│   └── run_tests.sh        # Script de testes
├── docker-compose.yml       # Ambiente local
├── Dockerfile              # Imagem Django
├── Dockerfile.celery       # Imagem Celery
├── requirements.txt        # Dependências Python
├── requirements-dev.txt    # Dependências de desenvolvimento
├── .pre-commit-config.yaml # Configuração pre-commit
├── pyproject.toml          # Configuração Black/isort
├── .flake8                 # Configuração flake8
├── k6_synthetic_tests.js   # Testes de carga K6
└── test_api_endpoints.sh   # Testes manuais de API
```

## 📚 Histórico de Desenvolvimento (PRs)

### PR #1: Base do Template Django
**Implementação inicial completa do template Django**
- ✅ Django 5.2 com Celery e RabbitMQ
- ✅ Observabilidade com Prometheus/Grafana
- ✅ Deployment Kubernetes
- ✅ GitHub Actions CI/CD
- ✅ Docker containerização
- ✅ Testes básicos

**Aprendizados:**
- Configuração Celery com RabbitMQ broker
- Middleware prometheus para métricas HTTP
- Estrutura de deployment Kubernetes
- Health checks para containers

### PR #2: Sistema de Autenticação JWT
**App de acesso completo com JWT e modelos de usuário**
- ✅ CustomUserModel com campos específicos (credits, stripe_id, etc.)
- ✅ JWT authentication com refresh tokens
- ✅ 6 modelos relacionados (LoggedDevice, PreRegister, etc.)
- ✅ API REST completa com CRUD
- ✅ 23 testes unitários
- ✅ Testes K6 sintéticos

**Modelos Implementados:**
```python
# access/models.py
CustomUserModel          # Usuário principal
ResetPasswordControl     # Controle reset senha
PasswordRecoveryEmail    # Templates de email
EmailConfirmationControl # Confirmação de email
PreRegister             # Pré-cadastro
LoggedDevice            # Dispositivos logados
```

**Endpoints de API:**
```python
# Autenticação
POST /api/access/auth/login/
POST /api/access/auth/refresh/

# Usuários
GET/POST/PUT/DELETE /api/access/users/
GET /api/access/users/me/

# Dispositivos
GET/POST/PUT/DELETE /api/access/logged-devices/
POST /api/access/logged-devices/{id}/update_login/

# Pré-registro (público)
GET/POST /api/access/pre-register/
```

### PR #3: Sistema de Qualidade de Código
**Pre-commit hooks e linting automático**
- ✅ Black para formatação automática
- ✅ flake8 para linting
- ✅ isort para organização de imports
- ✅ Pre-commit hooks git
- ✅ Execução de testes antes de commit

**Configurações:**
```yaml
# .pre-commit-config.yaml
- black (formatação)
- isort (imports)
- flake8 (linting)
- trailing-whitespace
- end-of-file-fixer
- django tests
```

### PR #4: Correção de Serializers
**Fix nos serializers de PasswordRecoveryEmail**
- ✅ Correção de mapeamento de campos
- ✅ Alinhamento com schema do banco
- ✅ Todos os testes passando (27/27)

**Erro Corrigido:**
```python
# ANTES (incorreto)
fields = ("id", "email", "sent_at")

# DEPOIS (correto)
fields = ("id", "name", "body", "subject", "email_adress")
```

### PR #5: Documentação Swagger/OpenAPI
**Documentação completa da API**
- ✅ drf-spectacular integration
- ✅ Swagger UI em /api/docs/
- ✅ ReDoc em /api/redoc/
- ✅ Schema OpenAPI em /api/schema/
- ✅ Documentação de modelos em /docs/
- ✅ Documentação de endpoints
- ✅ JWT authentication configurado

**Recursos de Documentação:**
```python
# URLs adicionados
/api/docs/    # Swagger UI interativo
/api/redoc/   # ReDoc documentation
/api/schema/  # Schema OpenAPI download
```

## 🔄 Fluxo de Desenvolvimento

### 1. Setup do Ambiente
```bash
# Clone do repositório
git clone https://github.com/williamkleber1/django_template.git
cd django_template

# Instalação de dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup pre-commit
pre-commit install

# Ambiente local com Docker
./dev.sh
# OU
docker-compose up -d
```

### 2. Desenvolvimento de Features

#### Branch Naming Convention
```bash
# Features
git checkout -b feature/nome-da-feature

# Bugfixes
git checkout -b bugfix/descricao-do-bug

# Melhorias
git checkout -b improvement/descricao-melhoria
```

#### Workflow de Commit
```bash
# Os pre-commit hooks automaticamente:
# 1. Formatam código com Black
# 2. Organizam imports com isort
# 3. Verificam linting com flake8
# 4. Executam testes Django

git add .
git commit -m "feat: adicionar nova funcionalidade"
# Pre-commit hooks executam automaticamente
```

### 3. Testes Durante Desenvolvimento
```bash
# Testes unitários
python manage.py test

# Testes específicos
python manage.py test access.tests.APITests.test_user_registration

# Testes com verbosidade
python manage.py test --verbosity=2

# Coverage (se instalado)
coverage run --source='.' manage.py test
coverage report
```

## 🎨 Convenções de Código

### Python/Django
- **Formatação:** Black (88 caracteres por linha)
- **Imports:** isort com perfil Django
- **Linting:** flake8 com regras Django
- **Docstrings:** Google style para classes e métodos importantes

```python
# Exemplo de model
class ExemploModel(BaseModel):
    """Modelo de exemplo seguindo padrões do projeto.
    
    Herda de BaseModel que fornece:
    - id (CharField UUID)
    - created (DateTimeField)
    - updated (DateTimeField)
    """
    nome = models.CharField(max_length=255, help_text="Nome do exemplo")
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Exemplo"
        verbose_name_plural = "Exemplos"
        ordering = ["-created"]
    
    def __str__(self):
        return self.nome
```

### API Endpoints
- **ViewSets:** Usar ViewSets do DRF para CRUD completo
- **Serializers:** Sempre validar dados de entrada
- **Permissions:** JWT authentication para endpoints protegidos
- **Documentation:** Usar decorators drf-spectacular

```python
# Exemplo de ViewSet
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

class ExemploViewSet(viewsets.ModelViewSet):
    """ViewSet para gestão de exemplos."""
    queryset = Exemplo.objects.all()
    serializer_class = ExemploSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Ação customizada",
        description="Executa ação específica no exemplo"
    )
    @action(detail=True, methods=['post'])
    def acao_customizada(self, request, pk=None):
        exemplo = self.get_object()
        # Lógica da ação
        return Response({"status": "sucesso"})
```

### Celery Tasks
- **Naming:** Prefixo com nome do app
- **Logging:** Sempre incluir logs nas tasks
- **Error Handling:** Try/catch com retry logic
- **Monitoring:** Métricas para task execution

```python
# Exemplo de task
import logging
from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def exemplo_task(self, param1, param2):
    """Task de exemplo com retry automático."""
    try:
        logger.info(f"Iniciando task exemplo com {param1}, {param2}")
        
        # Lógica da task
        resultado = fazer_processamento(param1, param2)
        
        logger.info(f"Task concluída com sucesso: {resultado}")
        return resultado
        
    except Exception as exc:
        logger.error(f"Erro na task: {exc}")
        raise self.retry(exc=exc, countdown=60)
```

## 🧪 Testes e Qualidade

### Estrutura de Testes

#### 1. Testes Unitários Django
```python
# access/tests.py - Exemplo de teste
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class APITests(APITestCase):
    """Testes da API de acesso."""
    
    def setUp(self):
        """Setup executado antes de cada teste."""
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    
    def test_user_registration(self):
        """Teste de registro de usuário."""
        url = reverse("customusermodel-list")
        response = self.client.post(url, self.user_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response.data)
    
    def test_authenticated_endpoint(self):
        """Teste de endpoint protegido."""
        # Criar usuário e obter token
        user = CustomUserModel.objects.create_user(**self.user_data)
        token = self.get_token_for_user(user)
        
        # Fazer request autenticado
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(reverse("customusermodel-me"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])
```

#### 2. Testes K6 Sintéticos
```javascript
// k6_synthetic_tests.js - Exemplo
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '10s', target: 2 },
    { duration: '30s', target: 5 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    http_req_failed: ['rate<0.1'],
  },
};

export default function () {
  // Teste de registro
  const registerResponse = http.post(`${BASE_URL}/api/access/users/`, {
    username: `user${Date.now()}`,
    email: `test${Date.now()}@example.com`,
    password: 'testpass123'
  });
  
  check(registerResponse, {
    'registration status is 201': (r) => r.status === 201,
    'has access token': (r) => JSON.parse(r.body).access_token !== undefined,
  });
  
  sleep(1);
}
```

#### 3. Execução de Testes

```bash
# Todos os testes unitários
python manage.py test

# Testes específicos por app
python manage.py test access
python manage.py test core

# Testes específicos por classe
python manage.py test access.tests.APITests

# Testes com coverage
coverage run --source='.' manage.py test
coverage html  # Gera relatório HTML

# Testes K6
k6 run k6_synthetic_tests.js

# Testes manuais de API
chmod +x test_api_endpoints.sh
./test_api_endpoints.sh
```

### Qualidade de Código

#### Pre-commit Hooks
```bash
# Executar manualmente
pre-commit run --all-files

# Verificar arquivos específicos
pre-commit run --files access/models.py

# Bypass em emergência (não recomendado)
git commit --no-verify -m "emergency fix"
```

#### Linting Manual
```bash
# Black - formatação
black .
black --check .  # Apenas verificar

# isort - imports
isort .
isort --check-only .

# flake8 - linting
flake8
flake8 access/  # App específico
```

## 📊 Monitoramento e Logs

### Configuração de Logs

#### Django Settings
```python
# django_app/settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'access': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

#### Uso de Logs no Código
```python
import logging

logger = logging.getLogger(__name__)

class ExemploViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        logger.info(f"Criando novo exemplo para usuário {request.user.id}")
        
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Exemplo criado com sucesso: {response.data['id']}")
            return response
        except Exception as e:
            logger.error(f"Erro ao criar exemplo: {str(e)}")
            raise

@shared_task
def processo_importante(dados):
    logger.info(f"Iniciando processo importante com {len(dados)} items")
    
    for item in dados:
        try:
            processar_item(item)
            logger.debug(f"Item processado: {item['id']}")
        except Exception as e:
            logger.error(f"Erro ao processar item {item['id']}: {str(e)}")
    
    logger.info("Processo importante concluído")
```

### Métricas Prometheus

#### Configuração django-prometheus
```python
# django_app/settings.py
INSTALLED_APPS = [
    'django_prometheus',  # Primeiro na lista
    # ... outros apps
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    # ... outros middlewares
    'django_prometheus.middleware.PrometheusAfterMiddleware',  # Último
]

# URLs
# django_app/urls.py
urlpatterns = [
    path('', include('django_prometheus.urls')),
    # ... outras URLs
]
```

#### Métricas Disponíveis
- **HTTP Requests:** Taxa, duração, status codes
- **Database:** Conexões, queries, performance
- **Celery:** Tasks executadas, sucesso/falha, duração
- **Sistema:** CPU, memória, disco

#### Acesso às Métricas
```bash
# Métricas Django
curl http://localhost:8000/metrics

# Métricas no Grafana
# http://localhost:3000 (admin/admin)
```

### Dashboards Grafana

#### Dashboards Pré-configurados
1. **Django Overview**
   - Taxa de requisições HTTP
   - Tempo de resposta médio
   - Status codes HTTP
   - Conexões de banco

2. **Celery Tasks**
   - Tasks por minuto
   - Taxa de sucesso/erro
   - Duração de tasks
   - Queue length

3. **Sistema**
   - CPU usage
   - Memory usage
   - Disk I/O
   - Container health

#### Customização de Dashboards
```yaml
# monitoring/grafana/dashboards/custom.json
{
  "dashboard": {
    "title": "Custom Django Dashboard",
    "panels": [
      {
        "title": "API Response Times",
        "type": "graph",
        "targets": [
          {
            "expr": "django_http_requests_duration_seconds_avg",
            "legendFormat": "Avg Response Time"
          }
        ]
      }
    ]
  }
}
```

## 🚀 Deployment e CI/CD

### GitHub Actions Pipeline

#### Configuração (.github/workflows/ci-cd.yml)
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
```

#### Secrets Necessários
```bash
# GitHub Secrets
KUBECONFIG          # Configuração do cluster K8s
REGISTRY_TOKEN      # Token para GitHub Container Registry
```

### Deployment Kubernetes

#### Local Development
```bash
# Ambiente local com Docker
./dev.sh

# Ou manualmente
docker-compose up -d

# Verificar serviços
docker-compose ps
```

#### Produção Kubernetes
```bash
# Deploy completo
kubectl apply -f k8s/

# Verificar deployment
kubectl get pods -n django-app
kubectl get services -n django-app

# Port forwarding para acesso
kubectl port-forward -n django-app service/django-service 8000:80
kubectl port-forward -n django-app service/grafana-service 3000:3000
```

#### Scaling
```bash
# Escalar Django pods
kubectl scale deployment django-deployment --replicas=3 -n django-app

# Escalar Celery workers
kubectl scale deployment celery-deployment --replicas=5 -n django-app
```

## 💡 Exemplos de Desenvolvimento

### 1. Adicionar Novo Endpoint de API

```python
# 1. Criar serializer
# access/serializers.py
class NovoRecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NovoRecurso
        fields = ['id', 'nome', 'descricao', 'ativo']

# 2. Criar ViewSet
# access/views.py
from drf_spectacular.utils import extend_schema

class NovoRecursoViewSet(viewsets.ModelViewSet):
    """Gestão de novos recursos."""
    queryset = NovoRecurso.objects.all()
    serializer_class = NovoRecursoSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Listar recursos",
        description="Lista todos os recursos do usuário autenticado"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# 3. Registrar URL
# access/urls.py
router.register(r'novos-recursos', NovoRecursoViewSet)

# 4. Criar testes
# access/tests.py
def test_novo_recurso_crud(self):
    """Teste CRUD completo do novo recurso."""
    self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
    
    # Create
    data = {"nome": "Teste", "descricao": "Descrição teste"}
    response = self.client.post("/api/access/novos-recursos/", data)
    self.assertEqual(response.status_code, 201)
    
    # Read
    recurso_id = response.data['id']
    response = self.client.get(f"/api/access/novos-recursos/{recurso_id}/")
    self.assertEqual(response.status_code, 200)
```

### 2. Adicionar Nova Celery Task

```python
# 1. Criar task
# core/tasks.py
@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def processar_dados_usuario(self, user_id, dados):
    """Processa dados do usuário de forma assíncrona."""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Processando dados para usuário {user_id}")
        
        user = CustomUserModel.objects.get(id=user_id)
        resultado = realizar_processamento(dados)
        
        # Atualizar usuário com resultado
        user.ultimo_processamento = timezone.now()
        user.save()
        
        logger.info(f"Processamento concluído para usuário {user_id}")
        return {"status": "sucesso", "resultado": resultado}
        
    except Exception as exc:
        logger.error(f"Erro no processamento: {exc}")
        raise self.retry(exc=exc, countdown=60)

# 2. Criar endpoint para disparar task
# core/views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def iniciar_processamento(request):
    """Inicia processamento assíncrono de dados."""
    dados = request.data.get('dados', [])
    
    # Disparar task
    task = processar_dados_usuario.delay(request.user.id, dados)
    
    return Response({
        "task_id": task.id,
        "status": "iniciado",
        "message": "Processamento iniciado com sucesso"
    })

# 3. Endpoint para verificar status
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def status_processamento(request, task_id):
    """Verifica status da task de processamento."""
    from celery.result import AsyncResult
    
    result = AsyncResult(task_id)
    
    return Response({
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    })

# 4. Adicionar às URLs
# core/urls.py
urlpatterns = [
    path('processar/', iniciar_processamento, name='iniciar_processamento'),
    path('status/<str:task_id>/', status_processamento, name='status_processamento'),
]

# 5. Teste da funcionalidade
# core/tests.py
def test_processamento_assincrono(self):
    """Teste de processamento assíncrono."""
    dados = [{"item": 1}, {"item": 2}]
    
    response = self.client.post('/processar/', {"dados": dados})
    self.assertEqual(response.status_code, 200)
    self.assertIn('task_id', response.data)
    
    # Verificar status
    task_id = response.data['task_id']
    response = self.client.get(f'/status/{task_id}/')
    self.assertEqual(response.status_code, 200)
```

### 3. Adicionar Monitoramento Customizado

```python
# 1. Métricas customizadas
# core/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Contadores
PROCESSAMENTOS_COUNTER = Counter(
    'django_processamentos_total',
    'Total de processamentos realizados',
    ['tipo', 'status']
)

# Histograma para duração
PROCESSAMENTO_DURATION = Histogram(
    'django_processamento_duration_seconds',
    'Duração dos processamentos em segundos',
    ['tipo']
)

# Gauge para items em queue
QUEUE_SIZE = Gauge(
    'django_queue_size',
    'Tamanho atual da queue',
    ['queue_name']
)

# 2. Uso nas tasks
# core/tasks.py
import time
from .metrics import PROCESSAMENTOS_COUNTER, PROCESSAMENTO_DURATION

@shared_task
def processar_com_metricas(dados):
    start_time = time.time()
    
    try:
        # Processamento
        resultado = fazer_processamento(dados)
        
        # Métricas de sucesso
        PROCESSAMENTOS_COUNTER.labels(tipo='dados', status='sucesso').inc()
        
        return resultado
        
    except Exception as e:
        # Métricas de erro
        PROCESSAMENTOS_COUNTER.labels(tipo='dados', status='erro').inc()
        raise
        
    finally:
        # Métrica de duração
        duration = time.time() - start_time
        PROCESSAMENTO_DURATION.labels(tipo='dados').observe(duration)

# 3. Endpoint de métricas customizadas
# core/views.py
from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

def metricas_customizadas(request):
    """Endpoint para métricas customizadas."""
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Celery não conecta ao RabbitMQ
```bash
# Verificar se RabbitMQ está rodando
docker-compose ps rabbitmq

# Logs do RabbitMQ
docker-compose logs rabbitmq

# Testar conexão
celery -A django_app inspect ping

# Solução: Verificar CELERY_BROKER_URL nas settings
```

#### 2. Testes falhando
```bash
# Verificar se banco de teste está limpo
python manage.py test --debug-mode

# Executar teste específico com mais detalhes
python manage.py test access.tests.APITests.test_user_registration --verbosity=2

# Resetar banco de teste
python manage.py flush --database=test
```

#### 3. Pre-commit hooks falhando
```bash
# Verificar o que está falhando
pre-commit run --all-files

# Corrigir formatação
black .
isort .

# Bypass temporário (não recomendado)
git commit --no-verify
```

#### 4. Problemas de Docker/Kubernetes
```bash
# Docker compose
docker-compose down
docker-compose up --build

# Kubernetes
kubectl delete pods --all -n django-app
kubectl apply -f k8s/

# Logs detalhados
kubectl logs -f deployment/django-deployment -n django-app
```

### Debug e Profiling

#### Django Debug
```python
# settings.py para debug
DEBUG = True
LOGGING['loggers']['django']['level'] = 'DEBUG'

# Debug de queries
LOGGING['loggers']['django.db.backends'] = {
    'level': 'DEBUG',
    'handlers': ['console'],
}
```

#### Celery Debug
```bash
# Modo verbose
celery -A django_app worker --loglevel=debug

# Monitor de tasks
celery -A django_app monitor

# Flower (se instalado)
celery -A django_app flower
```

### Performance

#### Database Optimization
```python
# Usar select_related para ForeignKeys
users = CustomUserModel.objects.select_related('subscription').all()

# Usar prefetch_related para ManyToMany
users = CustomUserModel.objects.prefetch_related('logged_devices').all()

# Índices no banco
class Meta:
    indexes = [
        models.Index(fields=['email']),
        models.Index(fields=['created', 'status']),
    ]
```

#### Celery Optimization
```python
# settings.py
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True
```

### Avisos Comuns do flake8

Alguns avisos do flake8 são comuns em projetos Django/DRF e são aceitáveis:

```bash
# E501 line too long - Comum em decorators DRF e docstrings
./access/views.py:29:89: E501 line too long (91 > 88 characters)

# Soluções:
# 1. Quebrar linha quando possível
@extend_schema(
    summary="Descrição curta",
    description="Descrição mais longa aqui"
)

# 2. Usar noqa para casos específicos
long_description = "String muito longa que não pode ser quebrada"  # noqa: E501

# 3. Configurar exceções no .flake8 para patterns Django
```

### Script de Validação

Use o script de validação para verificar se está seguindo as diretrizes:

```bash
# Executar validação completa
./scripts/validate_instructions.sh

# Saída esperada:
# ✅ Pre-commit configurado
# ✅ Todos os testes passaram (27/27)
# ✅ Formatação OK
# ✅ Imports organizados
# ✅ Instruções do Copilot disponíveis
# ✅ Diretório de documentação existe
```

## 📝 Conclusão

Este documento serve como guia completo para desenvolvimento com GitHub Copilot neste template Django. Todas as práticas documentadas foram validadas através dos PRs anteriores e garantem:

- ✅ **Qualidade de código** com pre-commit hooks automáticos
- ✅ **Testes abrangentes** com 27/27 testes passando
- ✅ **Monitoramento robusto** com Prometheus/Grafana
- ✅ **Deploy automatizado** com Kubernetes e GitHub Actions
- ✅ **Documentação atualizada** com Swagger/OpenAPI
- ✅ **Linting configurado** com Black, flake8 e isort
- ✅ **Script de validação** para verificar conformidade

### Como Usar Este Documento

1. **Para novos desenvolvimentos:** Siga os exemplos na seção "Exemplos de Desenvolvimento"
2. **Para debugging:** Use a seção "Troubleshooting"
3. **Para validação:** Execute `./scripts/validate_instructions.sh`
4. **Para referência:** Consulte as seções específicas conforme necessário

Para contribuições, sempre siga este documento e reference os PRs anteriores como exemplos de implementação.

---

**Última atualização:** Baseado nos PRs #1-#5  
**Versão Django:** 5.2.6  
**Versão DRF:** 3.15.2  
**Versão Celery:** 5.5.3  
**Testes:** 27/27 passando ✅