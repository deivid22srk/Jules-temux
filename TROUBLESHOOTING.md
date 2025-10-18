# 🔧 Guia de Troubleshooting - Jules Bot

## Problema: Erro 400 ao criar sessão

### Sintoma
```
❌ Erro ao criar sessão: 400 Client Error: Bad Request
```

### Causas e Soluções

#### 1. Repositório não conectado ao Jules

**Como identificar:**
- Use `/test` para testar a conexão
- Use `/sources` para ver repositórios disponíveis

**Solução:**
1. Acesse https://jules.google.com
2. Vá em Settings (Configurações)
3. Conecte seu repositório GitHub
4. Instale o Jules GitHub App no repositório
5. Aguarde alguns minutos para sincronizar
6. Use `/sources` novamente no bot

#### 2. Branch 'main' não existe no repositório

**Sintoma:**
```
Erro na Requisição!
• Branch 'main' não existe
```

**Solução:**
Seu repositório pode usar `master` ou outra branch padrão. Infelizmente, o bot atual só suporta branch `main`. Você pode:

**Opção A:** Renomear sua branch para `main` no GitHub:
```bash
git branch -m master main
git push -u origin main
git push origin --delete master
```

**Opção B:** Aguarde atualização do bot com suporte a outras branches.

#### 3. API Key inválida ou expirada

**Como identificar:**
Use `/test` - se aparecer "API Key Inválida", siga os passos:

**Solução:**
1. Acesse https://jules.google.com/settings#api
2. Revogue a chave antiga (se existir)
3. Gere uma nova API key
4. Edite o arquivo `jules_bot.py`:
   ```python
   JULES_API_KEY = "sua_nova_chave_aqui"
   ```
5. Reinicie o bot
6. Use `/test` novamente para confirmar

#### 4. Formato do source incorreto

**Formato correto:**
```
sources/github/USUARIO/REPOSITORIO
```

**Exemplos:**
✅ Correto:
```
/newsession sources/github/deivid22srk/Orion-Emulator Criar README
```

❌ Incorreto:
```
/newsession github.com/deivid22srk/Orion-Emulator Criar README
/newsession deivid22srk/Orion-Emulator Criar README
/newsession Orion-Emulator Criar README
```

**Dica:** Sempre use `/sources` e copie o nome exato!

---

## Problema: "Nenhum repositório encontrado"

### Sintoma
```
❌ Nenhum repositório encontrado.
```

### Solução Completa

#### Passo 1: Conectar repositório no Jules
1. Acesse https://jules.google.com
2. Faça login com sua conta Google
3. Clique em "Connect repository" ou ícone de engrenagem
4. Selecione "GitHub"
5. Autorize o Jules a acessar seu GitHub
6. Escolha os repositórios que deseja conectar

#### Passo 2: Instalar Jules GitHub App
1. No GitHub, vá em Settings > Applications
2. Encontre "Jules" nas GitHub Apps
3. Configure os repositórios que o Jules pode acessar
4. Salve as configurações

#### Passo 3: Aguardar sincronização
- Aguarde 2-5 minutos para o Jules sincronizar
- Use `/test` no bot para verificar
- Use `/sources` para listar repositórios

#### Passo 4: Verificar API Key
- A API key deve ser da mesma conta que conectou os repositórios
- Se você tem múltiplas contas Google, certifique-se de estar usando a key da conta certa

---

## Problema: Bot não responde no Telegram

### Sintoma
- Mensagens enviadas, mas bot não responde
- Bot offline

### Soluções

#### 1. Bot não está rodando
```bash
# Verifique se o bot está rodando
ps aux | grep jules_bot.py

# Se não estiver, inicie:
cd Jules-temux
python jules_bot.py
```

#### 2. Token do Telegram incorreto
```python
# Verifique no jules_bot.py:
TELEGRAM_BOT_TOKEN = "token_do_botfather"
```

**Como corrigir:**
1. Fale com @BotFather no Telegram
2. Use `/mybots`
3. Selecione seu bot
4. Clique em "API Token"
5. Copie o token
6. Substitua no `jules_bot.py`
7. Reinicie o bot

#### 3. Conexão com internet
```bash
# Teste conectividade
ping google.com

# Se não funcionar, verifique:
# - WiFi/dados móveis
# - Configurações de rede do Termux
```

---

## Problema: Modo auto-correção não funciona

### Sintoma
- Arquivos enviados, mas não analisados
- Sem resposta do DeepSeek

### Soluções

#### 1. Modo não ativado
```
/autocorrect on
```

#### 2. Nenhuma sessão ativa
```
# Primeiro crie uma sessão:
/newsession sources/github/user/repo Corrigir bugs

# Depois ative auto-correção:
/autocorrect on

# Agora envie os logs
```

#### 3. API Key OpenRouter incorreta
```python
# Verifique no jules_bot.py:
OPENROUTER_API_KEY = "sk-or-v1-..."
```

**Como obter:**
1. Acesse https://openrouter.ai
2. Faça login/cadastro
3. Vá em API Keys
4. Gere nova chave
5. Substitua no código
6. Reinicie o bot

#### 4. Formato do arquivo
- Apenas `.log` e `.txt` são aceitos
- Para outros formatos, copie o conteúdo e cole como texto

---

## Problema: "Activities" não mostram progresso

### Sintoma
```
❌ Nenhuma atividade encontrada.
```

### Possíveis causas

#### 1. Sessão ainda não iniciou
- Aguarde alguns segundos
- Use `/activities` novamente

#### 2. Session ID incorreto
```
# Use o ID exato retornado ao criar a sessão
/activities 12345678

# Ou simplesmente (usa a sessão atual):
/activities
```

#### 3. Sessão completada
- Use `/status` para ver o resultado final
- Verifique se foi criado um PR

---

## Problema: Jules demorado ou travado

### Sintoma
- Activities param de atualizar
- Sessão "congelada"

### Soluções

#### 1. Verifique o status
```
/activities <session_id>
```

Se mostrar atividades recentes, está funcionando (Jules pode demorar para tarefas complexas)

#### 2. Verifique no Jules Web
- Acesse https://jules.google.com
- Veja se a sessão está ativa lá
- Compare com o bot

#### 3. Crie nova sessão
Se realmente travou:
```
/newsession <source> <novo_prompt>
```

---

## Problema: Erro de permissão (403/401)

### Sintoma
```
❌ Erro de Autenticação!
PERMISSION_DENIED
```

### Soluções

#### 1. API Key expirada
```
/test
```

Se aparecer erro 401/403, gere nova key:
1. https://jules.google.com/settings#api
2. Delete chave antiga
3. Crie nova
4. Atualize no código
5. Reinicie bot

#### 2. Repositório privado sem permissão
- Certifique-se que o Jules GitHub App tem permissão no repo
- GitHub Settings > Applications > Jules > Configure
- Adicione o repositório específico

---

## Comandos de Diagnóstico

### Testar tudo
```
/test              # Testa conexão e API key
/sources          # Lista repositórios (se vazio, não conectou)
/sessions         # Lista sessões ativas
```

### Antes de criar sessão
```
1. /test          # ✅ Conexão OK?
2. /sources       # ✅ Repositório aparece?
3. /newsession... # Agora sim, crie!
```

---

## Checklist Completo de Setup

- [ ] Python instalado (`python --version`)
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Token Telegram configurado (fale com @BotFather)
- [ ] Jules API Key configurada (jules.google.com/settings#api)
- [ ] OpenRouter API Key configurada (openrouter.ai)
- [ ] Repositórios conectados no Jules (jules.google.com)
- [ ] Jules GitHub App instalado no repo (github.com/settings/applications)
- [ ] Bot rodando (`python jules_bot.py`)
- [ ] `/test` retorna sucesso
- [ ] `/sources` lista seus repositórios

---

## Logs do Bot

Para debugar problemas, veja os logs do bot:

```bash
# O bot imprime logs no terminal onde está rodando
# Procure por linhas com "ERROR" ou "Erro"

# Ou redirecione para arquivo:
python jules_bot.py > bot.log 2>&1
```

---

## Ainda com problemas?

### Informações para reportar

Se nada funcionar, colete estas informações:

1. **Versão Python:**
   ```bash
   python --version
   ```

2. **Resultado do /test:**
   (Screenshot ou copie a mensagem)

3. **Resultado do /sources:**
   (Screenshot ou copie a mensagem)

4. **Comando exato usado:**
   ```
   /newsession sources/github/...
   ```

5. **Erro completo:**
   (Screenshot ou copie a mensagem de erro)

6. **Logs do terminal:**
   (Últimas 10-20 linhas onde o bot está rodando)

---

## Dicas de Prevenção

### ✅ Faça sempre

1. Use `/test` antes de começar a usar o bot
2. Use `/sources` para copiar o nome exato do repo
3. Mantenha o bot rodando em tmux/nohup
4. Verifique `/activities` periodicamente
5. Use prompts descritivos e claros

### ❌ Evite

1. Não feche o terminal com o bot rodando (use tmux)
2. Não compartilhe suas API keys
3. Não use nomes de repositório sem verificar com `/sources`
4. Não espere respostas instantâneas (Jules demora para tarefas complexas)
5. Não crie múltiplas sessões para a mesma tarefa

---

## Recursos Úteis

- **Jules Web:** https://jules.google.com
- **Jules API Docs:** https://developers.google.com/jules/api
- **BotFather:** @BotFather (no Telegram)
- **OpenRouter:** https://openrouter.ai
- **Jules GitHub App:** https://github.com/apps/jules

---

**Última atualização:** 2025-10-18
