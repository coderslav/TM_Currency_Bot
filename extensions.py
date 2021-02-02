import requests
import json


class APIrequest:
    @staticmethod
    def get_price(what_convert, convert_to, amount):
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={what_convert}&tsyms={convert_to}")
        r_text = json.loads(r.content)
        float_price = float(*r_text.values())
        return f"{float_price * amount} {convert_to.upper()}"


class APIException(Exception):
    @staticmethod
    def message():
        return "Ошибка ввода или отсутствующая пара"
