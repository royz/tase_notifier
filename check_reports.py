import requests
from pprint import pprint
import datetime


def get_reports():
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1',
        'Accept-Language': 'he-IL',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.135 Safari/537.36',
        'X-Maya-With': 'allow',
        'Origin': 'https://maya.tase.co.il',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://maya.tase.co.il/reports/company',
    }

    response = requests.get('https://mayaapi.tase.co.il/api/report/company', headers=headers)

    top_reports = []
    for report in response.json()['Reports'][:5]:
        try:
            try:
                date = datetime.datetime.strptime(report['PubDate'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%H:%M %d/%m/%Y')
            except:
                date = report['PubDate']
            top_reports.append({
                'id': report['RptCode'],
                'text': report['Subject'],
                'date': date,
                'company': report['FormalCompanyData']['CompanyName']
            })
        except Exception as e:
            print(e)
            pass
    return top_reports


def render_reports(reports):
    pass


if __name__ == '__main__':
    while True:
        reports = get_reports()
        render_reports(reports)
