#!/usr/bin/env python3

import os
import json
import asyncio
import logging
from typing import Optional, Dict, Any
from datetime import datetime

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

JULES_API_KEY = "AQ.Ab8RN6LY7q3eWYwVUdQUWOCUJdzJO7EIvlCibJP3ZY-TO4-Xmg"
TELEGRAM_BOT_TOKEN = "8223002882:AAHc4n7whOcjw-BQhKry1X20Aqedxj9nGvM"
OPENROUTER_API_KEY = "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"

JULES_BASE_URL = "https://jules.googleapis.com/v1alpha"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

user_states = {}

class JulesAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'X-Goog-Api-Key': api_key,
            'Content-Type': 'application/json'
        }
    
    def list_sources(self, page_size: int = 10, page_token: Optional[str] = None) -> Dict:
        url = f"{JULES_BASE_URL}/sources"
        params = {'pageSize': page_size}
        if page_token:
            params['pageToken'] = page_token
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def create_session(self, prompt: str, source: str, starting_branch: str = "main", 
                      automation_mode: str = "MANUAL", require_plan_approval: bool = False,
                      title: Optional[str] = None) -> Dict:
        url = f"{JULES_BASE_URL}/sessions"
        data = {
            "prompt": prompt,
            "sourceContext": {
                "source": source,
                "githubRepoContext": {
                    "startingBranch": starting_branch
                }
            },
            "automationMode": automation_mode,
            "requirePlanApproval": require_plan_approval
        }
        if title:
            data["title"] = title
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def list_sessions(self, page_size: int = 10, page_token: Optional[str] = None) -> Dict:
        url = f"{JULES_BASE_URL}/sessions"
        params = {'pageSize': page_size}
        if page_token:
            params['pageToken'] = page_token
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_session(self, session_id: str) -> Dict:
        url = f"{JULES_BASE_URL}/sessions/{session_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def approve_plan(self, session_id: str) -> Dict:
        url = f"{JULES_BASE_URL}/sessions/{session_id}:approvePlan"
        response = requests.post(url, headers=self.headers, json={})
        response.raise_for_status()
        return response.json()
    
    def send_message(self, session_id: str, prompt: str) -> Dict:
        url = f"{JULES_BASE_URL}/sessions/{session_id}:sendMessage"
        data = {"prompt": prompt}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def list_activities(self, session_id: str, page_size: int = 30, 
                       page_token: Optional[str] = None) -> Dict:
        url = f"{JULES_BASE_URL}/sessions/{session_id}/activities"
        params = {'pageSize': page_size}
        if page_token:
            params['pageToken'] = page_token
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

class OpenRouterAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def analyze_logs(self, log_content: str) -> str:
        url = f"{OPENROUTER_BASE_URL}/chat/completions"
        data = {
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um assistente especializado em análise de logs de desenvolvimento de software. Analise os logs fornecidos e identifique erros, problemas e sugira correções específicas e acionáveis."
                },
                {
                    "role": "user",
                    "content": f"Analise os seguintes logs e forneça instruções claras e específicas para corrigir os problemas encontrados:\n\n{log_content}"
                }
            ]
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']

jules_api = JulesAPI(JULES_API_KEY)
openrouter_api = OpenRouterAPI(OPENROUTER_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {'auto_correction': False, 'current_session': None}
    
    welcome_message = """
🤖 *Bem-vindo ao Jules Bot!*

Este bot permite que você controle o Jules do Google diretamente pelo Telegram.

*Comandos disponíveis:*

📁 */sources* - Listar repositórios disponíveis
📝 */newsession* - Criar uma nova sessão
📋 */sessions* - Listar sessões ativas
💬 */message* - Enviar mensagem para uma sessão
📊 */activities* - Ver atividades de uma sessão
✅ */approve* - Aprovar plano de uma sessão
🔍 */status* - Ver status de uma sessão

🤖 *Modo Auto-Correção:*
*/autocorrect on* - Ativar modo de auto-correção
*/autocorrect off* - Desativar modo de auto-correção

Quando o modo de auto-correção está ativo, você pode enviar arquivos de log e o bot irá:
1. Analisar os logs com DeepSeek
2. Identificar problemas
3. Enviar instruções de correção para o Jules

*/help* - Ver esta mensagem novamente
"""
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def list_sources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Buscando repositórios disponíveis...")
    
    try:
        result = jules_api.list_sources(page_size=20)
        sources = result.get('sources', [])
        
        if not sources:
            await update.message.reply_text("❌ Nenhum repositório encontrado.")
            return
        
        message = "*📁 Repositórios disponíveis:*\n\n"
        for idx, source in enumerate(sources, 1):
            source_name = source.get('name', 'N/A')
            source_id = source.get('id', 'N/A')
            if 'githubRepo' in source:
                repo_info = source['githubRepo']
                owner = repo_info.get('owner', 'N/A')
                repo = repo_info.get('repo', 'N/A')
                message += f"{idx}. *{owner}/{repo}*\n"
                message += f"   `{source_name}`\n\n"
        
        if len(message) > 4000:
            chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, parse_mode='Markdown')
    
    except Exception as e:
        logger.error(f"Erro ao listar sources: {e}")
        await update.message.reply_text(f"❌ Erro ao listar repositórios: {str(e)}")

async def new_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ *Uso incorreto!*\n\n"
            "*Formato:* `/newsession <source> <prompt>`\n\n"
            "*Exemplo:*\n"
            "`/newsession sources/github/user/repo Adicionar funcionalidade de login`\n\n"
            "Use `/sources` para ver os repositórios disponíveis.",
            parse_mode='Markdown'
        )
        return
    
    source = context.args[0]
    prompt = ' '.join(context.args[1:])
    
    await update.message.reply_text(f"🚀 Criando sessão...\n\n*Prompt:* {prompt}")
    
    try:
        result = jules_api.create_session(
            prompt=prompt,
            source=source,
            starting_branch="main",
            automation_mode="MANUAL",
            require_plan_approval=False,
            title=prompt[:100]
        )
        
        session_id = result.get('id', 'N/A')
        session_name = result.get('name', 'N/A')
        
        user_id = update.effective_user.id
        if user_id not in user_states:
            user_states[user_id] = {}
        user_states[user_id]['current_session'] = session_id
        
        message = f"✅ *Sessão criada com sucesso!*\n\n"
        message += f"*ID:* `{session_id}`\n"
        message += f"*Nome:* {session_name}\n\n"
        message += f"Use `/activities {session_id}` para acompanhar o progresso."
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    except Exception as e:
        logger.error(f"Erro ao criar sessão: {e}")
        await update.message.reply_text(f"❌ Erro ao criar sessão: {str(e)}")

async def list_sessions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Buscando sessões...")
    
    try:
        result = jules_api.list_sessions(page_size=20)
        sessions = result.get('sessions', [])
        
        if not sessions:
            await update.message.reply_text("❌ Nenhuma sessão encontrada.")
            return
        
        message = "*📋 Sessões ativas:*\n\n"
        for idx, session in enumerate(sessions, 1):
            session_id = session.get('id', 'N/A')
            title = session.get('title', 'Sem título')
            prompt = session.get('prompt', 'N/A')
            
            message += f"{idx}. *{title}*\n"
            message += f"   ID: `{session_id}`\n"
            message += f"   Prompt: _{prompt[:50]}..._\n\n"
        
        if len(message) > 4000:
            chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, parse_mode='Markdown')
    
    except Exception as e:
        logger.error(f"Erro ao listar sessões: {e}")
        await update.message.reply_text(f"❌ Erro ao listar sessões: {str(e)}")

async def send_message_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if len(context.args) < 1:
        current_session = user_states.get(user_id, {}).get('current_session')
        if not current_session:
            await update.message.reply_text(
                "⚠️ *Uso incorreto!*\n\n"
                "*Formato:* `/message <session_id> <mensagem>`\n\n"
                "*Exemplo:*\n"
                "`/message 12345678 Adicione testes unitários`",
                parse_mode='Markdown'
            )
            return
        else:
            session_id = current_session
            message_text = ' '.join(context.args)
    else:
        session_id = context.args[0]
        message_text = ' '.join(context.args[1:])
    
    if not message_text:
        await update.message.reply_text("❌ Você precisa fornecer uma mensagem!")
        return
    
    await update.message.reply_text(f"💬 Enviando mensagem para sessão `{session_id}`...", parse_mode='Markdown')
    
    try:
        jules_api.send_message(session_id, message_text)
        await update.message.reply_text(
            f"✅ Mensagem enviada!\n\n"
            f"Use `/activities {session_id}` para ver a resposta.",
            parse_mode='Markdown'
        )
    
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {e}")
        await update.message.reply_text(f"❌ Erro ao enviar mensagem: {str(e)}")

async def list_activities_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if len(context.args) < 1:
        current_session = user_states.get(user_id, {}).get('current_session')
        if not current_session:
            await update.message.reply_text(
                "⚠️ *Uso incorreto!*\n\n"
                "*Formato:* `/activities <session_id>`\n\n"
                "*Exemplo:*\n"
                "`/activities 12345678`",
                parse_mode='Markdown'
            )
            return
        session_id = current_session
    else:
        session_id = context.args[0]
    
    await update.message.reply_text(f"📊 Buscando atividades da sessão `{session_id}`...", parse_mode='Markdown')
    
    try:
        result = jules_api.list_activities(session_id, page_size=10)
        activities = result.get('activities', [])
        
        if not activities:
            await update.message.reply_text("❌ Nenhuma atividade encontrada.")
            return
        
        message = f"*📊 Atividades da sessão {session_id}:*\n\n"
        for idx, activity in enumerate(activities, 1):
            originator = activity.get('originator', 'N/A')
            create_time = activity.get('createTime', 'N/A')
            
            icon = "🤖" if originator == "agent" else "👤"
            message += f"{icon} *Atividade {idx}* ({originator})\n"
            message += f"   Hora: {create_time}\n"
            
            if 'planGenerated' in activity:
                plan = activity['planGenerated'].get('plan', {})
                steps = plan.get('steps', [])
                message += f"   📋 Plano gerado ({len(steps)} passos)\n"
            
            elif 'progressUpdated' in activity:
                progress = activity['progressUpdated']
                title = progress.get('title', 'N/A')
                message += f"   ⚙️ {title}\n"
            
            elif 'sessionCompleted' in activity:
                message += f"   ✅ Sessão completada!\n"
            
            elif 'planApproved' in activity:
                message += f"   ✅ Plano aprovado\n"
            
            message += "\n"
        
        if len(message) > 4000:
            chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, parse_mode='Markdown')
    
    except Exception as e:
        logger.error(f"Erro ao listar atividades: {e}")
        await update.message.reply_text(f"❌ Erro ao listar atividades: {str(e)}")

async def approve_plan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if len(context.args) < 1:
        current_session = user_states.get(user_id, {}).get('current_session')
        if not current_session:
            await update.message.reply_text(
                "⚠️ *Uso incorreto!*\n\n"
                "*Formato:* `/approve <session_id>`\n\n"
                "*Exemplo:*\n"
                "`/approve 12345678`",
                parse_mode='Markdown'
            )
            return
        session_id = current_session
    else:
        session_id = context.args[0]
    
    await update.message.reply_text(f"✅ Aprovando plano da sessão `{session_id}`...", parse_mode='Markdown')
    
    try:
        jules_api.approve_plan(session_id)
        await update.message.reply_text(
            f"✅ Plano aprovado com sucesso!\n\n"
            f"Use `/activities {session_id}` para acompanhar o progresso.",
            parse_mode='Markdown'
        )
    
    except Exception as e:
        logger.error(f"Erro ao aprovar plano: {e}")
        await update.message.reply_text(f"❌ Erro ao aprovar plano: {str(e)}")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if len(context.args) < 1:
        current_session = user_states.get(user_id, {}).get('current_session')
        if not current_session:
            await update.message.reply_text(
                "⚠️ *Uso incorreto!*\n\n"
                "*Formato:* `/status <session_id>`\n\n"
                "*Exemplo:*\n"
                "`/status 12345678`",
                parse_mode='Markdown'
            )
            return
        session_id = current_session
    else:
        session_id = context.args[0]
    
    await update.message.reply_text(f"🔍 Buscando status da sessão `{session_id}`...", parse_mode='Markdown')
    
    try:
        session = jules_api.get_session(session_id)
        
        message = "*🔍 Status da Sessão*\n\n"
        message += f"*ID:* `{session.get('id', 'N/A')}`\n"
        message += f"*Título:* {session.get('title', 'N/A')}\n"
        message += f"*Prompt:* {session.get('prompt', 'N/A')}\n\n"
        
        if 'outputs' in session and session['outputs']:
            message += "*📤 Outputs:*\n"
            for output in session['outputs']:
                if 'pullRequest' in output:
                    pr = output['pullRequest']
                    message += f"  🔗 PR: [{pr.get('title', 'N/A')}]({pr.get('url', '#')})\n"
        
        await update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=True)
    
    except Exception as e:
        logger.error(f"Erro ao buscar status: {e}")
        await update.message.reply_text(f"❌ Erro ao buscar status: {str(e)}")

async def autocorrect_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {'auto_correction': False, 'current_session': None}
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "⚠️ *Uso incorreto!*\n\n"
            "*Formato:* `/autocorrect <on|off>`\n\n"
            "*Exemplo:*\n"
            "`/autocorrect on` - Ativa o modo de auto-correção\n"
            "`/autocorrect off` - Desativa o modo de auto-correção",
            parse_mode='Markdown'
        )
        return
    
    mode = context.args[0].lower()
    
    if mode == 'on':
        user_states[user_id]['auto_correction'] = True
        await update.message.reply_text(
            "✅ *Modo de auto-correção ATIVADO!*\n\n"
            "Agora você pode:\n"
            "1. Enviar arquivos de log (.txt, .log)\n"
            "2. O bot irá analisar com DeepSeek\n"
            "3. Enviar instruções de correção para o Jules\n\n"
            "Certifique-se de ter uma sessão ativa com `/newsession`",
            parse_mode='Markdown'
        )
    elif mode == 'off':
        user_states[user_id]['auto_correction'] = False
        await update.message.reply_text(
            "❌ *Modo de auto-correção DESATIVADO!*",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "⚠️ Opção inválida! Use `on` ou `off`.",
            parse_mode='Markdown'
        )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in user_states or not user_states[user_id].get('auto_correction', False):
        await update.message.reply_text(
            "⚠️ O modo de auto-correção está desativado.\n"
            "Use `/autocorrect on` para ativar.",
            parse_mode='Markdown'
        )
        return
    
    current_session = user_states[user_id].get('current_session')
    if not current_session:
        await update.message.reply_text(
            "⚠️ Nenhuma sessão ativa!\n"
            "Use `/newsession` para criar uma sessão primeiro.",
            parse_mode='Markdown'
        )
        return
    
    document = update.message.document
    file_name = document.file_name
    
    if not (file_name.endswith('.log') or file_name.endswith('.txt')):
        await update.message.reply_text(
            "⚠️ Apenas arquivos .log ou .txt são suportados!"
        )
        return
    
    await update.message.reply_text(f"📄 Recebendo arquivo: {file_name}...")
    
    try:
        file = await context.bot.get_file(document.file_id)
        file_path = f"/tmp/{file_name}"
        await file.download_to_drive(file_path)
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            log_content = f.read()
        
        await update.message.reply_text("🤖 Analisando logs com DeepSeek...")
        
        analysis = openrouter_api.analyze_logs(log_content)
        
        analysis_message = f"*🔍 Análise dos Logs:*\n\n{analysis}"
        if len(analysis_message) > 4000:
            chunks = [analysis_message[i:i+4000] for i in range(0, len(analysis_message), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode='Markdown')
        else:
            await update.message.reply_text(analysis_message, parse_mode='Markdown')
        
        await update.message.reply_text(
            f"📤 Enviando instruções de correção para Jules (sessão `{current_session}`)...",
            parse_mode='Markdown'
        )
        
        correction_prompt = f"Com base na análise dos logs, por favor corrija os seguintes problemas:\n\n{analysis}"
        jules_api.send_message(current_session, correction_prompt)
        
        await update.message.reply_text(
            "✅ *Instruções enviadas com sucesso!*\n\n"
            f"Use `/activities {current_session}` para acompanhar o progresso.",
            parse_mode='Markdown'
        )
        
        os.remove(file_path)
    
    except Exception as e:
        logger.error(f"Erro ao processar documento: {e}")
        await update.message.reply_text(f"❌ Erro ao processar arquivo: {str(e)}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in user_states or not user_states[user_id].get('auto_correction', False):
        return
    
    current_session = user_states[user_id].get('current_session')
    if not current_session:
        return
    
    text = update.message.text
    
    if len(text) > 200 and ('error' in text.lower() or 'exception' in text.lower() or 'traceback' in text.lower()):
        await update.message.reply_text("📄 Detectei um possível log. Analisando...")
        
        try:
            await update.message.reply_text("🤖 Analisando com DeepSeek...")
            
            analysis = openrouter_api.analyze_logs(text)
            
            analysis_message = f"*🔍 Análise:*\n\n{analysis}"
            if len(analysis_message) > 4000:
                chunks = [analysis_message[i:i+4000] for i in range(0, len(analysis_message), 4000)]
                for chunk in chunks:
                    await update.message.reply_text(chunk, parse_mode='Markdown')
            else:
                await update.message.reply_text(analysis_message, parse_mode='Markdown')
            
            await update.message.reply_text(
                f"📤 Enviando correções para Jules (sessão `{current_session}`)...",
                parse_mode='Markdown'
            )
            
            correction_prompt = f"Com base na análise dos logs, por favor corrija:\n\n{analysis}"
            jules_api.send_message(current_session, correction_prompt)
            
            await update.message.reply_text(
                "✅ *Instruções enviadas!*\n\n"
                f"Use `/activities {current_session}` para acompanhar.",
                parse_mode='Markdown'
            )
        
        except Exception as e:
            logger.error(f"Erro ao processar texto: {e}")
            await update.message.reply_text(f"❌ Erro: {str(e)}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Erro: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            f"❌ Ocorreu um erro inesperado:\n{str(context.error)}"
        )

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("sources", list_sources))
    application.add_handler(CommandHandler("newsession", new_session))
    application.add_handler(CommandHandler("sessions", list_sessions_command))
    application.add_handler(CommandHandler("message", send_message_command))
    application.add_handler(CommandHandler("activities", list_activities_command))
    application.add_handler(CommandHandler("approve", approve_plan_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("autocorrect", autocorrect_command))
    
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    application.add_error_handler(error_handler)
    
    logger.info("Bot iniciado! Aguardando mensagens...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
