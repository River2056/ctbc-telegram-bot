import logging
import requests
from datetime import datetime
from datetime import timedelta

# telegram related
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram import Update
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

updater = Updater(token='5167551581:AAHPZW0gnnPn2RD5xOzNFpJgmBpGbqJjX8E', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    kb = [
        [KeyboardButton('/on')],
        [KeyboardButton('/off')]
    ]
    kb_markup = ReplyKeyboardMarkup(kb)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to ctbc punch card telegram bot!', reply_markup=kb_markup)

def get_time_str(current_time):
    year = current_time.year
    month = current_time.month if current_time.month >= 10 else f'0{current_time.month}'
    day = current_time.date().day if current_time.date().day >= 10 else f'0{current_time.date().day}'
    hour = current_time.hour if current_time.hour >= 10 else f'0{current_time.hour}'
    min= current_time.minute if current_time.minute >= 10 else f'0{current_time.minute}'
    return f'{year}-{month}-{day} {hour}:{min}'

def start_working(update: Update, context: CallbackContext):
    current_time = datetime.now()
    # add 8 hours for aws server
    # current_time += timedelta(hours=8)
    time_str = get_time_str(current_time)
    payload = {
        'ownerId': 1,
        'startTime': time_str,
    }

    # send api request
    res = requests.post('http://localhost:8080/start', json=payload)
    reply = ''
    if res.status_code == 200:
        reply = f'Success, {time_str}'
    else:
        reply = f'Failed, {time_str}, check log for details'
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

def end_working(update: Update, context: CallbackContext):
    current_time = datetime.now()
    # add 8 hours for aws server
    # current_time += timedelta(hours=8)
    time_str = get_time_str(current_time)
    payload = {
        'ownerId': 1,
        'endTime': time_str,
    }

    # send api request
    res = requests.post('http://localhost:8080/end', json=payload)
    reply = ''
    if res.status_code == 200:
        reply = f'Success, {time_str}'
    else:
        reply = f'Failed, {time_str}, check log for details'
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

start_handler = CommandHandler('start', start)
start_working_handler = CommandHandler('on', start_working)
end_working_handler = CommandHandler('off', end_working)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(start_working_handler)
dispatcher.add_handler(end_working_handler)

# run bot
updater.start_polling()

# run the bot until user presses Ctrl-C or process receives SIGINT, SIGTERM or SIGABRT
updater.idle()
