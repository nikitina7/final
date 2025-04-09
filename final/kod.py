import telebot
import random
import time
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = "7885782864:AAGfTvOlKb05N1uRzNklIgohrKxA3ixtlYs"
bot = telebot.TeleBot(TOKEN)

ECO_TIPS = [
    "Выключай свет, когда выходишь из комнаты.",
    "Используй многоразовую бутылку вместо пластиковой.",
    "Отдай старую одежду на благотворительность вместо выбрасывания.",
    "Экономь воду: закрывай кран, когда чистишь зубы.",
    "Откажись от пластиковых пакетов – используй многоразовые сумки.",
]

subscribers = set()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который поможет тебе заботиться об экологии. "
                                     "Отправь /совет, чтобы получить экологический совет, или /подписка, чтобы получать советы ежедневно.")

@bot.message_handler(commands=['совет'])
def send_advice(message):
    bot.send_message(message.chat.id, random.choice(ECO_TIPS))

@bot.message_handler(commands=['подписка'])
def subscribe(message):
    subscribers.add(message.chat.id)
    bot.send_message(message.chat.id, "Вы подписаны на ежедневные советы.")

@bot.message_handler(commands=['отписка'])
def unsubscribe(message):
    subscribers.discard(message.chat.id)
    bot.send_message(message.chat.id, "Вы отписались от рассылки.")

def send_daily_tips():
    for user_id in subscribers:
        try:
            bot.send_message(user_id, random.choice(ECO_TIPS))
        except Exception as e:
            print(f"Ошибка при отправке сообщения {user_id}: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_tips, 'interval', hours=24)
scheduler.start()

bot.polling(none_stop=True)
