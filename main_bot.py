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
import set_bot
import requests
import json

TOKEN = set_bot.token
bot = telebot.TeleBot(TOKEN)
available_pairs = {"eur": "eur", "euro": "eur", "евро": "eur",
                   "usd": "usd", "dollar": "usd", "доллар": "usd",
                   "uah": "uah", "hryvna": "uah", "гривна": "uah",
                   "rub": "rub", "ruble": "rub", "рубль": "rub",
                   "btc": "btc", "bitcoin": "btc", "биткоин": "btc",
                   "eth": "eth", "ethereum": "eth", "эфириум": "eth",
                   "dot": "dot", "polkadot": "dot", "полкадот": "dot"}

help_message = "Введите сначала валюту, которую вы хотите конвертировать, далее через пробел - валюту в которую " \
               "конвертируете и в конце так же через пробел количество переводимой валюты. Например, вы хотите " \
               "конвертироваться 100 Долларов в Биткоин. Для этого вам нужно написать следующую команду:" \
               "\nUSD BTC 100\nВы так же можете ввести полные названия валют на английском или русском языках. " \
               "Удачи! :)\n\nСписок доступных команд для бота:\n/start - перезагрузка бота" \
               "\n/help - помощь\n/values  - список доступных для конвертации валют"


@bot.message_handler(commands=['start', 'help', 'values'])
def start_help_values(message):
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
def convert(message):
    global available_pairs
    try:
        what_convert, convert_to, amount = message.text.lower().split(" ")
        try:
            amount = int(amount)
        except ValueError:
            bot.send_message(message.from_user.id, "Ошибка! Введите, пожалуйста, числовое значение суммы")
        else:
            if what_convert not in available_pairs or convert_to not in available_pairs:
                bot.send_message(message.from_user.id, "К сожалению, я не могу вам помочь \U0001F614 Отсутствующая "
                                                       "валютная пара или введены неверные значения")
            else:
                bot.reply_to(message, f"{message.from_user.first_name}, тестируем {available_pairs[what_convert]},"
                                      f" {available_pairs[convert_to]}, {amount}")
                r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={available_pairs[what_convert]}"
                                 f"&tsyms={available_pairs[convert_to]}")
                r_text = json.loads(r.content)
                print(int(*r_text.values()) * amount)
    except ValueError:
        bot.send_message(message.from_user.id, "Ошибка! Введите, пожалуйста, значение в формате:\n\n<валюта>_<валюта, "
                                               "в которую конвертируете>_<сумма>\n\nБез треугольных скобок, а вместо "
                                               "нижнего подчеркивания \"_\" поставьте пробел")


@bot.message_handler(content_types=['photo'])
def photos(message: telebot.types.Message):
    bot.reply_to(message, "Nice meme XDD")


bot.polling(none_stop=True, interval=0)
