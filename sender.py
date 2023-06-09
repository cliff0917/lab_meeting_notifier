import os
import time
import json
import glob
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import policy
from datetime import datetime, timedelta

class LabMeetingEmailSender:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file

    def load_config(self):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def get_content(self, first_part, second_part):
        first_part = first_part.split('將於 ')[-1]
        first_part = first_part.replace('在', '將於')
        email_text = f"實驗室同仁大家好：\n\n"
        email_text += f"{first_part}\n\n{second_part}\n\n"
        email_text += "<個人進度> https://goo.gl/YN2h4d\n"
        email_text += "<計畫進度> https://goo.gl/dcE87S\n"
        email_text += "<會議簡報> https://reurl.cc/DdgY9m"
        return email_text

    def send_lab_seminar_reminder(self):
        chinese = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '日'}
        no_network = 0

        while True:
            # get today's info
            today = datetime.today().isoweekday()
            now = datetime.now()
            cur_time = now.strftime("%H:%M")

            # get config
            self.load_config()
            stop = self.config['stop']
            send_weekday = self.config['send_weekday']
            send_time = self.config['send_time']

            # 若有網路且為寄信日期和時間 => 寄信
            # 若沒網路但是為寄信日期, 則不斷嘗試寄信, 一旦在寄信日期內重連上網路, 成功寄出信後, 把狀態設回有網路
            if (no_network == 0 and today == send_weekday and cur_time == send_time) or \
               (no_network == 1 and today == send_weekday):

                if stop:
                    print('本週暫停寄信')
                    time.sleep(518100)  # 86400 * 6 - 300
                    continue

                # get tomorrow's info
                tomorrow = now + timedelta(days=1)
                month, day = [int(i) for i in tomorrow.strftime("%m/%d").split('/')]

                ############################## setting ##############################
                meeting_time = self.config['meeting_time']
                classroom = self.config['classroom']
                deadline = meeting_time - 1
                first_part = f'Lab Seminar 將於 {month}/{day}({chinese[send_weekday % 7 + 1]}) {meeting_time}:00 在 {classroom} 進行會議'
                second_part = f'請在 {deadline}:00 前提供進度'
                title = f'{first_part}，{second_part}'

                email_text = self.get_content(first_part, second_part)
                ####################################################################

                send_path = '.'
                cc_csv = f'{send_path}/老師和助理.csv'

                # 老師和助理為副本(cc)
                if os.path.isfile(cc_csv):
                    df = pd.read_csv(cc_csv)
                    info = [f"{df['name'].iloc[i]} <{df['email'].iloc[i]}>" for i in range(len(df))]
                    cc = ", ".join(info)

                # receiver
                all_grades = sorted(glob.glob(f'{send_path}/*.csv'))
                try:
                    all_grades.remove(f'{send_path}/老師和助理.csv')
                except:
                    pass

                for i in range(len(all_grades)):
                    df = pd.read_csv(all_grades[i])
                    info = [f"{df['name'].iloc[i]} <{df['email'].iloc[i]}>" for i in range(len(df))]
                    if i == 0:
                        receiver = ", ".join(info)
                    else:
                        receiver += ", " + ", ".join(info)

                content = MIMEMultipart(policy=policy.default)
                content['subject'] = title  # title
                content['from'] = 'usccbot@gmail.com'  # sender
                content['to'] = receiver  # receiver
                try:
                    content['cc'] = cc
                except:
                    pass
                content.attach(MIMEText(email_text))

                try:
                    with smtplib.SMTP(host='smtp.gmail.com', port='587') as smtp:
                        try:
                            smtp.ehlo()  # 驗證 SMTP
                            smtp.starttls()  # 建立加密傳輸
                            smtp.login('usccbot@gmail.com', 'nkotcvbljpfybxko')  # login sender gmail
                            smtp.send_message(content)  # send email
                            no_network = 0  # 成功寄出代表有網路
                            print("會議提醒信已寄出!")
                            time.sleep(518100)  # 86400 * 6 - 300
                        except Exception as e:
                            print('Error message: ', e)
                except:
                    no_network = 1  # smtp 設定失敗代表沒有網路
                    time.sleep(60)

            # 如果沒網路, 但是已是寄信日的隔天 => 則不寄, 等到下週再寄
            elif no_network == 1 and today == send_weekday + 1:
                time.sleep(518100)  # 86400 * 6 - 300

            # 有網路, 但不為寄信的日期、時間 or 沒網路, 且不為寄信的日期
            else:
                time.sleep(60)