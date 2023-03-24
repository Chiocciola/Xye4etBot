import os, re, atexit, json
from collections import defaultdict
import logging
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

regex = re.compile(r'\b(н[aаeеи]|[дп][oо]|з?[aа]|[cс]|[oо](т|дн[oо])?)?([xх]|}{|[kк][cс])[yу]([eеёийюя]|ли(?!ган|о)).*?\b', re.IGNORECASE)

class ChatData(object):
    def __init__(self):
        self.counters = defaultdict(int)

chats = defaultdict(ChatData)

#atexit.register(lambda: json.dump(chats, open('data.json', 'w')))

async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatData = chats[update.message.chat.id]

    if len(chatData.counters) > 0:
        await update.message.chat.send_message('*Таблица хуёв*\n' + '\n'.join([f'{name}: {count}' for name, count in chatData.counters.items()]), parse_mode=constants.ParseMode.MARKDOWN_V2)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatData = chats[update.message.chat.id]
    chatData.counters.clear() 

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
  
    chatData = chats[update.message.chat.id]

    if regex.search(update.message.text):
        chatData.counters[update.message.from_user.full_name] += 1
        await update.message.chat.send_chat_action(constants.ChatAction.TYPING)

if __name__ == '__main__':

    logging.basicConfig(filename='application.log', filemode='w', format='%(asctime)s [%(levelname)s] %(name)s - %(message)s', level=logging.INFO)#, encoding='UTF-8')

    application = ApplicationBuilder().token(os.environ['Telegram_API_KEY']).build()

    application.add_handler(CommandHandler('stat', stat))
    application.add_handler(CommandHandler('reset', reset))
    application.add_handler(MessageHandler(filters.TEXT, messages))

    application.run_polling()