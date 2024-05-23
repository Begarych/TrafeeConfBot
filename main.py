import asyncio

import telebot.types
# import telebot.types
from telebot import TeleBot
from telebot.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardRemove)
from telebot.async_telebot import AsyncTeleBot
from utils import Registry
from config import TOKEN, allowed_user_ids
from time import sleep

# bot = AsyncTeleBot(TOKEN)
bot = TeleBot(TOKEN)
session = Registry()


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    # session.register_status = False
    session.user_id = message.from_user.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Продолжить"))
    bot.send_message(message.chat.id, text=f'Привет, {message.chat.first_name}! 🙋‍♂\n\n️Это Trafee Conf Bot, который '
                                                 f'поможет тебе с регистрацией на конкурс. Чтобы начать, жми кнопку '
                                                 f'"Продолжить" ниже ⬇️',
                                                 reply_markup=markup)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message: telebot.types.Message):
    if message.from_user.id not in allowed_user_ids:
        bot.reply_to(message, "У вас нет прав на выполнение этой команды.")
        return

    if not session.get_xml_field("id"):
        bot.reply_to(message, "xml файл пустой")
        return
    session.broadcast_status = True
    bot.send_message(message.chat.id, text="Введите текст для рассылки")


@bot.message_handler(func=lambda message: session.broadcast_status and message.from_user.id in allowed_user_ids)
def distribution(message: telebot.types.Message):
    for user in session.get_xml_field("id"):
        try:
            bot.send_message(user, message.text)
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user}: {e}")
    session.broadcast_status = False


@bot.message_handler(func=lambda message: message.text == "Продолжить")
def instruction(message: telebot.types.Message):
    bot.send_message(message.chat.id, text="📨 Введите ваш адрес электронной почты\n\n Пример: example@example.com",
                           reply_markup=ReplyKeyboardRemove())
    session.message_status[message.chat.id] = "waiting"


@bot.message_handler(func=lambda message: session.message_status[message.chat.id] == "waiting")
def user_data_handler(message: telebot.types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Да"), KeyboardButton("Нет"))
    session.user_mail = message.text
    bot.send_message(message.chat.id, text=f"Это ваш электронный адрес: \n{session.user_mail}", reply_markup=markup)
    session.message_status[message.chat.id] = "done"


@bot.message_handler(func=lambda message: message.text == "Нет")
def try_again(message: telebot.types.Message):
    session.user_mail = None
    instruction(message)


@bot.message_handler(func=lambda message: message.text == "Да" and not session.register_status)
def confirmed(message: telebot.types.Message):
    session.write_to_xml(message.chat.first_name, str(session.user_id), session.user_mail)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(url="https://www.trafee.com/publisher/register", text="Ссылка"))
    session.register_status = True
    bot.send_message(message.chat.id, text=f"📩 Ваш адрес электронной почты успешно сохранен.",
                           reply_markup=ReplyKeyboardRemove())
    bot.send_message(message.chat.id, text=f"Чтобы завершить регистрацию, пожалуйста, перейдите по ссылке",
                           reply_markup=keyboard)
    sleep(10)
    bot.send_message(message.chat.id, text="Не забудьте проверить и подтвердить свой электронный адрес. Также, "
                                                 "приглашаем вас присоединиться к нашему Telegram-каналу 📲, где сейчас "
                                                 "идет топовый розыгрыш премиум-аккаунтов. Не пропустите!\n"
                                                 "https://t.me/trafeeRuChanel",
                           reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: session.register_status)
async def already_register(message: telebot.types.Message):
    bot.send_message(message.chat.id, text="Вы уже были зарегистрированы\n"
                                                 "Не забудьте проверить и подтвердить свой электронный адрес. Также, "
                                                 "приглашаем вас присоединиться к нашему Telegram-каналу 📲, где сейчас "
                                                 "идет топовый розыгрыш премиум-аккаунтов. Не пропустите!\n"
                                                 "https://t.me/trafeeRuChanel"
                           )


@bot.message_handler(func=lambda message: True)
def useless(message: telebot.types.Message):
    bot.send_message(message.chat.id, text="Используйте /start для старта бота")


# asyncio.run(bot.polling(none_stop=True, skip_pending=True))


bot.polling(none_stop=True, skip_pending=True)
