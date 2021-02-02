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
available_commands = "Список доступных команд:\n/start - перезагрузка бота\n/help - помощь\n/values  - доступные для " \
                     "конвертации валюты"
help_message = f"\U000027A1 Сначала введите валюту, которую хотите конвертировать\n\U000027A1 Далее, через пробел — " \
               f"валюту, в которую конвертируете\n\U000027A1 В конце, также через пробел, количество переводимой " \
               f"валюты\n\n\U0001F7E2 Например, вы хотите конвертировать 100 Долларов в Биткоин Для этого нужно " \
               f"написать следующую команду:\n\nUSD BTC 100\n\nВы также можете ввести полные названия валют на " \
               f"английском или русском языках\n\n{available_commands}"


@bot.message_handler(commands=['start', 'help', 'values'])
def start_help_values(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, f"Здравствуй, {message.from_user.first_name}! Добро пожаловать в "
                                               f"конвертвер Фиатных и Крипто валют! Пользоваться им довольно просто:\n"
                                               f"\n{help_message}")

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
            bot.send_message(message.from_user.id, f"\U000026D4 Ошибка!\n\n\U00002705Введите, пожалуйста, числовое "
                                                   f"значение суммы\n\U00002705Если число дробное - используйте точку, "
                                                   f"а не запятую в качестве разделителя\n\n{available_commands}")
        else:
            try:
                if what_convert not in available_pairs or convert_to not in available_pairs or amount < 0:
                    raise extensions.APIException

            except extensions.APIException:
                bot.send_message(message.from_user.id, f"К сожалению, я не могу вам помочь \U0001F614\nВалютная пара "
                                                       f"отсутствует или введены неверные значения\n\n\U0001F4A1 "
                                                       f"Обратите внимание, что введенная сумма не должна быть "
                                                       f"отрицательной\n\n{available_commands}")
            else:
                price = extensions.APIrequest.get_price(available_pairs[what_convert], available_pairs[convert_to],
                                                        amount)
                bot.reply_to(message, price)
    except ValueError:
        bot.send_message(message.from_user.id, f"\U000026D4 Ошибка!\n\n\U00002705Введите, пожалуйста, значение в "
                                               f"формате:\n\n <валюта>_<валюта, в которую конвертируете>_<сумма>"
                                               f"\n\n\U00002705 Без треугольных скобок, а вместо нижнего "
                                               f"подчеркивания \"_\" поставьте пробел\n\n{available_commands}")


@bot.message_handler(content_types=['photo', 'audio', 'document', 'sticker', 'video', 'location', 'contact', ])
def other_content(message: telebot.types.Message):
    bot.reply_to(message, f"Простите, но я принимаю только текстовый ввод \U0001F937\n\n{available_commands}")


bot.polling()
