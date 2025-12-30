import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
from datetime import datetime
import os

TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 704717451
bot = telebot.TeleBot(TOKEN)

def menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🔨 Замер", callback_data='1'))
    markup.add(InlineKeyboardButton("📞 Консультация", callback_data='2'))
    markup.add(InlineKeyboardButton("🔧 Монтаж", callback_data='3'))
    markup.add(InlineKeyboardButton("🏠 Настройка HiTE PRO", callback_data='4'))
    markup.add(InlineKeyboardButton("📙 Главное меню", callback_data='0'))
    return markup

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "🏠 Добро пожаловать в HiTE PRO Kazan!\n\nВыберите услугу:", reply_markup=menu())

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.answer_callback_query(call.id)
    if call.data == '0':
        bot.edit_message_text("🏠 Выберите услугу:", call.message.chat.id, call.message.message_id, reply_markup=menu())
        return
    services = {'1': '🔨 Замер', '2': '📞 Консультация', '3': '🔧 Монтаж', '4': '🏠 Настройка HiTE PRO'}
    bot.send_message(call.message.chat.id, f"{services[call.data]}\n\n👤 Введите ваше имя:")
    bot.register_next_step_handler(call.message, process_name, call.data)

def process_name(message, service_id):
    name = message.text.strip()
    bot.send_message(message.chat.id, "📱 Введите номер телефона:")
    bot.register_next_step_handler(message, process_phone, service_id, name)

def process_phone(message, service_id, name):
    phone = message.text.strip()
    if not re.match(r'^(\+7|8|7)?[\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', phone):
        bot.send_message(message.chat.id, "❌ Неверный формат!\nПример: +79991234567\nПовторите:")
        bot.register_next_step_handler(message, process_phone, service_id, name)
        return
    services = {'1': '🔨 Замер', '2': '📞 Консультация', '3': '🔧 Монтаж', '4': '🏠 Настройка HiTE PRO'}
    msg = f"🎉 НОВАЯ ЗАЯВКА!\n\n{services[service_id]}\n👤 {name}\n📱 {phone}\n⏰ {datetime.now().strftime('%d.%m %H:%M')}\n🆔 {message.from_user.id}"
    bot.send_message(ADMIN_ID, msg)
    bot.send_message(message.chat.id, "✅ Заявка отправлена!\nМенеджер перезвонит в течение 30 минут!", reply_markup=menu())

if __name__ == '__main__':
    print("🚀 Бот HiTE PRO Kazan vFINAL запущен!")
    bot.polling(none_stop=True)
