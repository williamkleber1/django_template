#!/bin/bash

# Script de validação do COPILOT_INSTRUCTIONS.md
# Este script demonstra como seguir as instruções documentadas

echo "🚀 Validando instruções do GitHub Copilot..."

# 1. Verificar pre-commit hooks
echo "📋 Verificando pre-commit hooks..."
if [ -f ".pre-commit-config.yaml" ]; then
    echo "✅ Pre-commit configurado"
else
    echo "❌ Pre-commit não encontrado"
fi

# 2. Executar testes
echo "🧪 Executando testes..."
python manage.py test --verbosity=0
if [ $? -eq 0 ]; then
    echo "✅ Todos os testes passaram"
else
    echo "❌ Alguns testes falharam"
    exit 1
fi

# 3. Verificar linting
echo "🎨 Verificando linting..."
flake8 --max-line-length=88 --exclude=migrations
if [ $? -eq 0 ]; then
    echo "✅ Linting OK"
else
    echo "❌ Problemas de linting encontrados"
fi

# 4. Verificar formatação
echo "🔧 Verificando formatação..."
black --check .
if [ $? -eq 0 ]; then
    echo "✅ Formatação OK"
else
    echo "⚠️  Código precisa ser formatado"
fi

# 5. Verificar imports
echo "📦 Verificando imports..."
isort --check-only .
if [ $? -eq 0 ]; then
    echo "✅ Imports organizados"
else
    echo "⚠️  Imports precisam ser organizados"
fi

# 6. Verificar estrutura de documentação
echo "📚 Verificando documentação..."
if [ -f "COPILOT_INSTRUCTIONS.md" ]; then
    echo "✅ Instruções do Copilot disponíveis"
else
    echo "❌ Instruções do Copilot não encontradas"
fi

if [ -d "docs/" ]; then
    echo "✅ Diretório de documentação existe"
else
    echo "❌ Diretório de documentação não encontrado"
fi

echo "🎉 Validação concluída!"