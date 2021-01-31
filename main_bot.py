# text
# audio
# document
# photo
# sticker
# video
# location
# contact
# new_chat_participant
# left_chat_participant
# new_chat_title
# new_chat_photo
# delete_chat_photo
# group_chat_created
import telebot

TOKEN = r"TOKEN"

bot = telebot.TeleBot(TOKEN)

help_message = "Введите сначала валюту, которую вы хотите конвертировать, далее через пробел - валюту в которую " \
               "конвертируете и в конце так же через пробел сумму валюты, которую конвертируете. Например, вы хотите " \
               "конвертироваться 100 Долларов в Биткоин. Для этого вам нужно написать следующую команду:" \
               "\nUSD BTC 100\nВы так же можете ввести полные названия валют на английском или русском языке. " \
               "Удачи! :)\n\nСписок доступных команд для бота:\n/start - перезагрузка бота" \
               "\n/help - помощь\n/values  - список доступных для конвертации валют"


@bot.message_handler(commands=['start', 'help', 'values'])
def start(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, f"Здравствуй, {message.from_user.first_name}! Добро пожаловать в "
                                               f"конвертвер Фиатных и Крипто валют!\nПользоваться им довольно просто."
                                               f"{help_message}")

    elif message.text == "/values":
        bot.send_message(message.from_user.id, "Список доступных для конвертации валют:\nEUR (Eвро/Euro)\nUSD "
                                               "(Доллар/Dollar)\nUAH (Гривна/Hryvna)\nRUB (Рубль/Ruble)\nBTC "
                                               "(Биткоин/Bitcoin)\nETH (Эфириум/Ethereum) \nDOT (Полкадот/Polkadot)")
    else:
        bot.send_message(message.from_user.id, help_message)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    bot.reply_to(message, f"{message.from_user.first_name}, тестируем")


@bot.message_handler(content_types=['photo'])
def photos(message: telebot.types.Message):
    bot.reply_to(message, "Nice meme XDD")


bot.polling(none_stop=True, interval=0)
