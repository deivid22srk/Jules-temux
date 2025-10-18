# Exemplos de Uso do Jules Bot

## Cenário 1: Corrigir Bug Urgente

### Situação
Você tem um bug em produção e precisa corrigi-lo rapidamente.

### Passos

1. **Criar sessão de correção**
```
/newsession sources/github/usuario/meu-projeto Corrigir erro 500 no endpoint de checkout
```

2. **Ativar auto-correção**
```
/autocorrect on
```

3. **Enviar logs do erro**
- Anexe o arquivo `error.log` do servidor
- Ou cole o traceback completo no chat

4. **Acompanhar correção**
```
/activities <session_id>
```

5. **Verificar PR gerado**
```
/status <session_id>
```

O Jules criará um PR com a correção automaticamente!

---

## Cenário 2: Adicionar Nova Funcionalidade

### Situação
Precisa adicionar autenticação OAuth ao projeto.

### Passos

1. **Criar sessão**
```
/newsession sources/github/usuario/projeto Implementar autenticação OAuth com Google
```

2. **Ver plano gerado**
```
/activities <session_id>
```

3. **Adicionar requisitos específicos**
```
/message <session_id> Use a biblioteca Passport.js e adicione suporte para refresh tokens
```

4. **Acompanhar progresso**
```
/activities <session_id>
```

5. **Verificar resultado**
```
/status <session_id>
```

---

## Cenário 3: Refatoração de Código

### Situação
O código está funcionando mas precisa de refatoração.

### Passos

1. **Criar sessão de refatoração**
```
/newsession sources/github/usuario/projeto Refatorar módulo de pagamentos seguindo clean code
```

2. **Ver atividades**
```
/activities <session_id>
```

3. **Pedir melhorias específicas**
```
/message <session_id> Adicione testes unitários com Jest e coverage mínimo de 80%
```

4. **Verificar resultado**
```
/status <session_id>
```

---

## Cenário 4: Debug Automatizado

### Situação
Testes estão quebrados e você precisa identificar o problema.

### Passos

1. **Criar sessão**
```
/newsession sources/github/usuario/projeto Investigar falha nos testes de integração
```

2. **Ativar auto-correção**
```
/autocorrect on
```

3. **Enviar output dos testes**
- Cole o output completo do `npm test`
- Ou anexe arquivo `test-results.log`

4. **Jules analisa e corrige**
O bot irá:
- Analisar os erros com DeepSeek
- Identificar a causa raiz
- Enviar instruções de correção para Jules
- Jules implementa as correções

5. **Verificar correções**
```
/activities <session_id>
/status <session_id>
```

---

## Cenário 5: Code Review Automatizado

### Situação
Você quer que o Jules revise código antes de fazer merge.

### Passos

1. **Criar sessão de review**
```
/newsession sources/github/usuario/projeto Revisar código do PR #123 focando em segurança e performance
```

2. **Ver análise**
```
/activities <session_id>
```

3. **Pedir correções específicas**
```
/message <session_id> Corrigir todos os problemas de segurança identificados
```

---

## Cenário 6: Migração de Tecnologia

### Situação
Migrar de JavaScript para TypeScript.

### Passos

1. **Criar sessão**
```
/newsession sources/github/usuario/projeto Migrar todos os arquivos .js para TypeScript com tipos completos
```

2. **Acompanhar migração**
```
/activities <session_id>
```

3. **Adicionar requisitos**
```
/message <session_id> Configure o tsconfig.json com strict mode e adicione tipos para todas as APIs externas
```

4. **Verificar resultado**
```
/status <session_id>
```

---

## Cenário 7: Correção em Lote de Issues

### Situação
Várias issues pequenas precisam ser corrigidas.

### Para cada issue:

```
/newsession sources/github/usuario/projeto Corrigir issue #45: botão de logout não funciona em mobile
```

Faça isso para múltiplas issues em paralelo!

---

## Cenário 8: Documentação Automática

### Situação
Código sem documentação adequada.

### Passos

1. **Criar sessão**
```
/newsession sources/github/usuario/projeto Adicionar JSDoc completo em todos os arquivos e gerar documentação HTML
```

2. **Verificar progresso**
```
/activities <session_id>
```

---

## Cenário 9: Otimização de Performance

### Situação
App lento, precisa otimizar.

### Passos

1. **Criar sessão com logs**
```
/newsession sources/github/usuario/projeto Otimizar performance do backend
```

2. **Ativar auto-correção**
```
/autocorrect on
```

3. **Enviar logs de profiling**
- Anexe resultados do profiler
- Cole métricas de performance

4. **Jules implementa otimizações**
```
/activities <session_id>
```

---

## Cenário 10: Setup de CI/CD

### Situação
Configurar pipeline de CI/CD.

### Passos

```
/newsession sources/github/usuario/projeto Configurar GitHub Actions com testes, lint, build e deploy automático
```

Jules irá:
- Criar workflow YAML
- Configurar testes automatizados
- Setup de deploy
- Configurar notificações

---

## Dicas Pro

### 1. Sessões Simultâneas
Você pode ter múltiplas sessões ativas:
```
/newsession sources/github/user/proj1 Feature A
/newsession sources/github/user/proj2 Feature B
```

### 2. Contexto nas Mensagens
Seja específico:
```
❌ /message 123 adiciona teste
✅ /message 123 Adicione testes unitários usando Jest para as funções de validação no arquivo validators.js
```

### 3. Auto-Correção Proativa
Com auto-correção ativa, cole erros diretamente no chat:
```
[Colar traceback completo]
```

### 4. Monitoramento Contínuo
Use `/activities` frequentemente para acompanhar:
```
/activities <session_id>
```

### 5. Verificação de PRs
Sempre verifique o PR gerado:
```
/status <session_id>
```

---

## Comandos Rápidos

### Ver todos os repos
```
/sources
```

### Ver todas as sessões
```
/sessions
```

### Criar sessão rápida
```
/newsession <source> <o que fazer>
```

### Ativar correção automática
```
/autocorrect on
```

### Ver progresso
```
/activities <id>
```

### Ver resultado final
```
/status <id>
```

---

## Atalhos de Produtividade

Após criar uma sessão, ela fica como "sessão atual". Você pode usar comandos sem especificar ID:

```
/newsession sources/github/user/proj Fix bug X
/activities  # Automaticamente usa a sessão atual
/message Adicione logs de debug  # Usa sessão atual
/status  # Usa sessão atual
```

---

## Troubleshooting Durante Uso

### Jules está demorando
```
/activities <session_id>  # Ver o que está fazendo
```

### Precisa mudar direção
```
/message <session_id> Na verdade, faça isso de outra forma: [nova abordagem]
```

### Plano precisa aprovação
```
/approve <session_id>
```

### Ver se gerou PR
```
/status <session_id>
```

---

## Integração com Workflow Diário

### Manhã
```
/sessions  # Ver o que está rodando
```

### Durante o dia
```
/autocorrect on  # Sempre ativo
[Colar erros conforme aparecem]
```

### Final do dia
```
/sessions  # Review do que foi feito
```

---

**Experimente! O Jules Bot é poderoso e quanto mais você usa, mais produtivo fica!**
