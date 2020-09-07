import requests
import datetime
import tkinter as tk
import tkinter.font as tk_font
import webbrowser
from playsound import playsound
import os
import time


def open_link(rep_id):
    webbrowser.open(f'https://maya.tase.co.il/reports/details/{rep_id}')


def get_reports():
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'DNT': '1',
        'Accept-Language': 'he-IL',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/85.0.4183.83 Safari/537.36',
        'X-Maya-With': 'allow',
        'Origin': 'https://maya.tase.co.il',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://maya.tase.co.il/reports/breakingannouncement',
    }

    try:
        response = requests.get('https://mayaapi.tase.co.il/api/report/breakingannouncement', headers=headers)
    except:
        print('request timed out. sleeping for 30 seconds...')
        time.sleep(30)
        return get_reports()

    top_reports = []
    for report in response.json()['Reports'][:5]:
        try:
            try:
                date = datetime.datetime.strptime(report['PubDate'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%H:%M %d/%m/%Y')
            except:
                date = report['PubDate']
            top_reports.append({
                'id': report['RptCode'],
                'text': report['Subject'].strip(),
                'date': date,
                'company': report['FormalCompanyData']['CompanyName'].strip()
            })
        except Exception as e:
            pass
    return top_reports


def render_reports(reports):
    for wd in root.winfo_children():
        wd.destroy()

    for i, report in enumerate(reports):
        main_frame = tk.Frame(master=root, padx=5, bg='#e1e1e1', highlightbackground="#cccccc",
                              highlightthickness=1)
        upper_frame = tk.Frame(master=main_frame, pady=3)
        tk.Label(upper_frame, text=f'{report["date"]}  ', font=fontStyle,
                 width=15, bg='#ff8e6e').grid(row=0, column=0, sticky=tk.W)
        tk.Label(upper_frame, text=report['company'], font=fontStyle, width=25, bg='#ff8e6e').grid(row=0, column=1)
        tk.Button(
            upper_frame, text='open link',
            command=lambda rep_id=report['id']: open_link(rep_id)
        ).grid(row=0, column=2, sticky=tk.E)

        lower_frame = tk.Frame(master=main_frame, pady=3)
        tk.Label(lower_frame, text=report['text'], font=fontStyle,
                 wraplength=400, anchor=tk.E, width=47).grid(row=0, column=0)
        upper_frame.grid(row=0, column=0, columnspan=2)
        lower_frame.grid(row=1, column=0)
        main_frame.grid(row=i, column=0)


def check_for_updates():
    global report_ids
    print('checking for updates...')

    reports = get_reports()
    new_report_ids = [report['id'] for report in reports]
    if not report_ids:
        report_ids = new_report_ids
        render_reports(reports)
    else:
        if report_ids != new_report_ids:
            report_ids = new_report_ids
            print('reports updated')
            playsound(sound_file)
            render_reports(reports)
        else:
            pass
    root.after(3000, check_for_updates)


if __name__ == '__main__':
    sound_file = os.path.join(os.path.dirname(__file__), 'beep.mp3')
    root = tk.Tk()
    root.title("Check Reports")
    root.resizable(False, False)
    fontStyle = tk_font.Font(size=12)
    report_ids = None

    check_for_updates()
    root.mainloop()
