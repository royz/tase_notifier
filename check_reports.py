import requests

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'DNT': '1',
    'Accept-Language': 'he-IL',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'X-Maya-With': 'allow',
    'Origin': 'https://maya.tase.co.il',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://maya.tase.co.il/reports/company',
}

idx = 1
while True:
    response = requests.get('https://mayaapi.tase.co.il/api/report/company', headers=headers)
    print(idx, response.text, sep='. ')
    idx += 1
