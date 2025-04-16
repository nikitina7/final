import telebot
import random
import time
from apscheduler.schedulers.background import BackgroundScheduler
from telebot import types

TOKEN = "7885782864:AAGfTvOlKb05N1uRzNklIgohrKxA3ixtlYs"
bot = telebot.TeleBot(TOKEN)

ECO = [
    "Чаще ходи пешком или пользуйся велосипедом вместо машины.",
    "Используй общественный транспорт, чтобы сократить выбросы CO₂.",
    "Выключай электроприборы полностью, а не оставляй в режиме ожидания.",
    "Сортируй мусор и сдавай перерабатываемые материалы.",
    "Покупай местные продукты — это снижает углеродный след от транспорта.",
    "Сократи потребление мяса — животноводство сильно влияет на климат.",
    "Посади дерево — оно поглощает углекислый газ.",
    "Используй энергоэффективные лампы и бытовую технику.",
    "Уменьши использование кондиционеров и отопления — одевайся по погоде.",
    "Переходи на возобновляемые источники энергии, если есть возможность.",
    "Выключай свет, когда выходишь из комнаты.",
    "Используй многоразовую бутылку вместо пластиковой.",
    "Отдай старую одежду на благотворительность вместо выбрасывания.",
    "Экономь воду: закрывай кран, когда чистишь зубы.",
    "Откажись от пластиковых пакетов – используй многоразовые сумки.",
]

subscribers = set()

def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/совет")
    btn2 = types.KeyboardButton("/подписка")
    btn3 = types.KeyboardButton("/отписка")
    keyboard.add(btn1, btn2, btn3)
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Я бот, который поможет тебе заботиться об экологии 🌍\n\n"
                     "Нажми кнопку ниже или введи команду:\n"
                     "📌 /совет – получить экологический совет\n"
                     "✅ /подписка – получать советы каждый день\n"
                     "❌ /отписка – отменить подписку",
                     reply_markup=main_keyboard())

@bot.message_handler(commands=['совет'])
def send_advice(message):
    bot.send_message(message.chat.id, random.choice(ECO))

@bot.message_handler(commands=['подписка'])
def subscribe(message):
    subscribers.add(message.chat.id)
    bot.send_message(message.chat.id, "Вы подписаны на ежедневные советы 🌱")

@bot.message_handler(commands=['отписка'])
def unsubscribe(message):
    subscribers.discard(message.chat.id)
    bot.send_message(message.chat.id, "Вы отписались от рассылки 📴")

def send_daily_tips():
    for user_id in subscribers:
        try:
            bot.send_message(user_id, random.choice(ECO))
        except Exception as e:
            print(f"Ошибка при отправке сообщения {user_id}: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_tips, 'interval', hours=24)
scheduler.start()

bot.polling(none_stop=True)
