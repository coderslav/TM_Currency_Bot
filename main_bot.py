import telebot
import launch_bot
import extensions

TOKEN = launch_bot.token
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
               "\n\nСписок доступных команд для бота:\n/start - перезагрузка бота" \
               "\n/help - помощь\n/values  - список доступных для конвертации валют"


@bot.message_handler(commands=['start', 'help', 'values'])
def start_help_values(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, f"Здравствуй, {message.from_user.first_name}! Добро пожаловать в "
                                               f"конвертвер Фиатных и Крипто валют!\nПользоваться им довольно просто."
                                               f"{help_message}")

    elif message.text == "/values":
        bot.send_message(message.from_user.id, "Список доступных для конвертации валют:\n\nEUR (Eвро/Euro)\nUSD "
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
            amount = float(amount)
        except ValueError:
            bot.send_message(message.from_user.id, "Ошибка! Введите, пожалуйста, числовое значение суммы")
        else:
            try:
                if what_convert not in available_pairs or convert_to not in available_pairs or amount < 0:
                    raise extensions.APIException

            except extensions.APIException:
                bot.send_message(message.from_user.id, "К сожалению, я не могу вам помочь \U0001F614 Отсутствующая "
                                                       "валютная пара или введены неверные значения.\nОбратите "
                                                       "внимание, что введенная сумма не должна быть отрицательной "
                                                       "\U0000261D\nЧтобы ознакомиться с доступными для конвертации "
                                                       "валютными парами, введите /values")
            else:
                price = extensions.APIrequest.get_price(available_pairs[what_convert], available_pairs[convert_to],
                                                        amount)
                bot.reply_to(message, price)
    except ValueError:
        bot.send_message(message.from_user.id, "Ошибка! Введите, пожалуйста, значение в формате:\n\n<валюта>_<валюта, "
                                               "в которую конвертируете>_<сумма>\n\nБез треугольных скобок, а вместо "
                                               "нижнего подчеркивания \"_\" поставьте пробел")


@bot.message_handler(content_types=['photo', 'audio', 'document', 'sticker', 'video', 'location', 'contact', ])
def other_content(message: telebot.types.Message):
    bot.reply_to(message, "Простите, но я принимаю только текстовый ввод \U0001F937")


bot.polling()
