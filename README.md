# Jules Bot - Telegram Bot para Termux

Bot do Telegram que permite controlar o Jules do Google diretamente pelo Telegram, executável no Termux. Com suporte a modo de auto-correção usando DeepSeek para análise de logs.

## 🌟 Funcionalidades

### Comandos Principais

- **📁 Repositórios**
  - `/sources` - Listar todos os repositórios disponíveis conectados ao Jules

- **📝 Sessões**
  - `/newsession <source> <prompt>` - Criar nova sessão de trabalho
  - `/sessions` - Listar todas as sessões ativas
  - `/status <session_id>` - Ver status detalhado de uma sessão
  - `/activities <session_id>` - Visualizar atividades de uma sessão

- **💬 Interação**
  - `/message <session_id> <mensagem>` - Enviar mensagem para uma sessão
  - `/approve <session_id>` - Aprovar plano de execução

- **🤖 Auto-Correção**
  - `/autocorrect on` - Ativar modo de auto-correção
  - `/autocorrect off` - Desativar modo de auto-correção

### Modo de Auto-Correção

Quando ativado, o bot automaticamente:
1. Recebe arquivos de log (.txt, .log) ou texto com erros
2. Analisa os logs usando DeepSeek V3 via OpenRouter
3. Identifica problemas e erros
4. Envia instruções específicas de correção para o Jules
5. O Jules corrige automaticamente com base nas instruções

## 📦 Instalação no Termux

### Método Automático

```bash
# Clone o repositório
git clone https://github.com/deivid22srk/Jules-temux.git
cd Jules-temux

# Execute o script de instalação
chmod +x install.sh
./install.sh
```

### Método Manual

```bash
# Atualize os pacotes do Termux
pkg update && pkg upgrade -y

# Instale Python
pkg install python -y

# Instale pip e atualize
pip install --upgrade pip

# Instale as dependências
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Obter as Chaves API

#### Jules API Key
1. Acesse [jules.google.com/settings#api](https://jules.google.com/settings#api)
2. Crie uma nova API key
3. Copie a chave gerada

#### Token do Bot Telegram
1. No Telegram, fale com [@BotFather](https://t.me/BotFather)
2. Use o comando `/newbot`
3. Siga as instruções e copie o token

#### OpenRouter API Key
1. Acesse [openrouter.ai](https://openrouter.ai)
2. Crie uma conta ou faça login
3. Vá em API Keys e gere uma nova chave

### 2. Configurar o Bot

Edite o arquivo `jules_bot.py` e substitua as credenciais:

```python
JULES_API_KEY = "sua_jules_api_key_aqui"
TELEGRAM_BOT_TOKEN = "seu_telegram_bot_token_aqui"
OPENROUTER_API_KEY = "sua_openrouter_api_key_aqui"
```

Ou crie um arquivo `.env` (recomendado):

```bash
cp .env.example .env
nano .env
```

E preencha com suas credenciais:

```env
JULES_API_KEY=sua_jules_api_key
TELEGRAM_BOT_TOKEN=seu_telegram_bot_token
OPENROUTER_API_KEY=sua_openrouter_api_key
```

## 🚀 Executando o Bot

```bash
# No diretório do bot
python jules_bot.py
```

O bot ficará ativo e aguardando comandos!

## 📱 Como Usar

### 1. Iniciar o Bot

1. Abra o Telegram
2. Procure pelo seu bot (nome que você definiu no BotFather)
3. Envie `/start` para começar

### 2. Listar Repositórios

```
/sources
```

Isso mostrará todos os repositórios GitHub conectados ao seu Jules.

### 3. Criar uma Sessão

```
/newsession sources/github/usuario/repo Implementar sistema de login
```

Isso criará uma nova sessão de trabalho com o Jules.

### 4. Acompanhar Progresso

```
/activities 12345678
```

Substitua `12345678` pelo ID da sessão retornado no passo anterior.

### 5. Enviar Mensagens

```
/message 12345678 Adicione testes unitários para a função de login
```

### 6. Modo Auto-Correção

#### Ativar

```
/autocorrect on
```

#### Usar

Depois de ativado, simplesmente:

1. **Envie um arquivo de log:**
   - Anexe um arquivo .txt ou .log com os erros
   - O bot analisa automaticamente

2. **Cole o erro diretamente:**
   - Cole o texto do erro/traceback
   - Se contiver palavras como "error", "exception" ou "traceback", será processado automaticamente

3. **O bot fará:**
   - Análise com DeepSeek
   - Envio das correções para o Jules
   - Notificação quando completo

## 🔧 Exemplos de Uso Completo

### Exemplo 1: Corrigir um Bug

```
1. /newsession sources/github/usuario/projeto Corrigir bug no login
2. /autocorrect on
3. [Enviar arquivo error.log]
4. /activities 12345678 (para ver o progresso)
5. /status 12345678 (para ver se gerou PR)
```

### Exemplo 2: Adicionar Funcionalidade

```
1. /newsession sources/github/usuario/projeto Adicionar sistema de notificações
2. /activities 12345678
3. /message 12345678 Use Firebase Cloud Messaging
4. /activities 12345678
```

### Exemplo 3: Revisar Código

```
1. /newsession sources/github/usuario/projeto Revisar código do módulo de autenticação
2. /activities 12345678
3. /approve 12345678 (se necessário aprovar plano)
4. /status 12345678
```

## 🔐 Segurança

⚠️ **IMPORTANTE**: As chaves API são sensíveis! 

- Nunca compartilhe suas chaves
- Não comite arquivos com chaves no GitHub
- Use variáveis de ambiente quando possível
- O arquivo `.env` está no `.gitignore` por padrão

## 🐛 Solução de Problemas

### Bot não inicia

```bash
# Verifique se todas as dependências estão instaladas
pip install -r requirements.txt

# Verifique as credenciais
python -c "from jules_bot import JULES_API_KEY, TELEGRAM_BOT_TOKEN; print('OK')"
```

### Erro de conexão

- Verifique sua conexão com a internet
- Confirme se as chaves API estão corretas
- Verifique se o Jules está acessível

### Comandos não funcionam

- Certifique-se de que o bot está rodando
- Verifique os logs no terminal
- Use `/help` para ver comandos disponíveis

## 📚 Documentação Adicional

- [API do Jules](https://developers.google.com/jules/api)
- [Python Telegram Bot](https://python-telegram-bot.org/)
- [OpenRouter](https://openrouter.ai/docs)

## 🔄 Manter o Bot Rodando

### No Termux

Para manter o bot rodando em background:

```bash
# Instale o tmux
pkg install tmux

# Inicie uma sessão tmux
tmux new -s julesbot

# Execute o bot
python jules_bot.py

# Pressione Ctrl+B depois D para desanexar
# Para retornar: tmux attach -t julesbot
```

### Com nohup

```bash
nohup python jules_bot.py > bot.log 2>&1 &
```

## 🎯 Fluxo de Trabalho Recomendado

1. **Conecte seus repositórios** no [jules.google.com](https://jules.google.com)
2. **Liste os sources** com `/sources`
3. **Crie uma sessão** com `/newsession`
4. **Ative auto-correção** com `/autocorrect on`
5. **Monitore com** `/activities` e `/status`
6. **Envie correções** enviando logs quando necessário

## 📊 Estrutura do Projeto

```
Jules-temux/
├── jules_bot.py          # Bot principal
├── config.py             # Configurações (opcional)
├── requirements.txt      # Dependências Python
├── install.sh           # Script de instalação
├── .env.example         # Exemplo de variáveis de ambiente
└── README.md            # Esta documentação
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir funcionalidades
- Enviar pull requests

## 📝 Licença

Este projeto é de código aberto para uso pessoal e educacional.

## 🆘 Suporte

Se encontrar problemas:

1. Verifique a seção de Solução de Problemas
2. Consulte os logs do bot
3. Verifique a documentação da API do Jules

## ✨ Recursos Futuros

- [ ] Suporte a múltiplas sessões simultâneas
- [ ] Interface web para monitoramento
- [ ] Notificações automáticas de progresso
- [ ] Integração com mais modelos de IA
- [ ] Suporte a comandos inline
- [ ] Dashboard de estatísticas

---

**Desenvolvido para uso no Termux com integração Jules + DeepSeek**
