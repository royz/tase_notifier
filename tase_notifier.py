import datetime
import time
import requests
from playsound import playsound


def get_date():
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1',
        'Accept-Language': 'he-IL',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.135 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.tase.co.il',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.tase.co.il/he/market_data/indices/updates/parameters/listed_capital?isAdd=1',
    }

    data = '{"TotalRec":1,"pageNum":1,"lang":"0"}'

    try:
        response = requests.post('https://api.tase.co.il/api/index/listedcapital',
                                 headers=headers, data=data)
        return response.json()['TradeDate']

    except Exception as e:
        print(e)


def notify(new_date, updated_on):
    print(f'Changed on: {updated_on}')
    print(f'Date now is: {new_date}')


if __name__ == '__main__':
    first_date = None

    while True:
        new_date = get_date()
        if not first_date:
            first_date = new_date
            print(f'current date is {first_date}. checking for updates every 30 seconds...')

        if new_date != first_date:
            updated_on = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print(updated_on)
            time.sleep(240)
            notify(new_date, updated_on)
            playsound('beep.mp3')
            first_date = new_date
        else:
            time.sleep(30)
