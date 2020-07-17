import telebot
from telebot import types

bot = telebot.TeleBot('') # Token
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Cancel', '/reg')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2.row('Привет', 'Пока')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет, ты прописал команду /start, для того чтобы узнать команды бота введите команду /command')


@bot.message_handler(commands=['exit'])
def exit_message(message):
    bot.send_message(message.chat.id, 'Прощай')


@bot.message_handler(commands=['command'])
def command_message(message):
    bot.send_message(message.chat.id, 'Вот команды', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'cancel':
        bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAIB9F8R2liaaKV79YmkqFGKQxQoQjSzAAJQAQACqCEhBrG98bXN6YSiGgQ')
    elif message.text.lower() == '/help':
        bot.send_message(message.chat.id, 'Хелповик', reply_markup=keyboard2)
    elif message.text.lower() == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю напиши /help')


name = ''
surname = ''
age = 0


def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)
    bot.send_message(message.chat.id, 'id стикера', )


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Запомню : )')
    elif call.data == "no":
        ...  # переспрашиваем


bot.polling()
