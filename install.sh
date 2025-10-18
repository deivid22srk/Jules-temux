#!/bin/bash

echo "🚀 Instalando Jules Bot no Termux..."
echo ""

echo "📦 Atualizando pacotes..."
pkg update -y && pkg upgrade -y

echo "🐍 Instalando Python..."
pkg install python -y

echo "📚 Instalando pip..."
pip install --upgrade pip

echo "📦 Instalando dependências do bot..."
pip install -r requirements.txt

echo "✅ Instalação concluída!"
echo ""
echo "📝 Para executar o bot, use:"
echo "   python jules_bot.py"
echo ""
echo "⚠️  Certifique-se de ter configurado as variáveis de ambiente em .env"
