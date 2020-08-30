import os
import time
import ctypes
import datetime
import requests
import webbrowser
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


def Mbox(title, text, style):
    try:
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)
    except Exception as e:
        print(f'failed to initialize message box. [{" ".join(str(e).split())}]')
        return None


def notify(new_date, updated_on):
    sound_file = os.path.join(os.path.dirname(__file__), 'beep.mp3')
    playsound(sound_file)
    msg = f'Changed on: {updated_on}\nDate now is: {new_date}'
    return Mbox('Date changed', msg, 1)


if __name__ == '__main__':
    first_date = None

    while True:
        try:
            new_date = get_date()
            updated_on = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            if not first_date:
                first_date = new_date
                print(f'current date is {first_date}. checking for updates every 30 seconds...')

            if new_date != first_date:
                print(f'{updated_on} | date has updated. waiting for 4 minutes before notifying...')
                time.sleep(240)
                open_browser = notify(new_date, updated_on) == 1
                if open_browser:
                    print('opening link in a browser...')
                    webbrowser.open(
                        'https://www.tase.co.il/he/market_data/indices/updates/parameters/listed_capital?isAdd=1', 2)
                else:
                    print('closing script...')
                quit(0)
            else:
                print(f'{updated_on} | date has not updated. [current date: {new_date}]')
                time.sleep(30)
        except Exception as e:
            print(e)
