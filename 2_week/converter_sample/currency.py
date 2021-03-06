from bs4 import BeautifulSoup
from decimal import Decimal
import requests

def convert(amount, cur_from, cur_to, date, requests):
    API = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req={dat}'.format(dat = date)
    response = requests.get(API)  # Использовать переданный requests

    soup = BeautifulSoup(response.content, 'xml')

    if cur_from != 'RUR':
        val_from = Decimal(soup.find('CharCode' , text=cur_from).find_next_sibling('Value').string.replace(',','.'))
        nom_from = Decimal(soup.find('CharCode' , text=cur_from).find_next_sibling('Nominal').string.replace(',','.'))
    else:
        val_from = Decimal(1.0)
        nom_from = Decimal(1.0)

    if cur_to != 'RUR':
        val_to = Decimal(soup.find('CharCode' , text=cur_to).find_next_sibling('Value').string.replace(',', '.'))
        nom_to = Decimal(soup.find('CharCode' , text=cur_to).find_next_sibling('Nominal').string.replace(',','.'))
    else:
        val_to = Decimal(1.0)
        nom_to = Decimal(1.0)


    result = (amount * val_from / nom_from * nom_to / val_to).quantize(Decimal("1.0000"))
    return result  # не забыть про округление до 4х знаков после запятой



