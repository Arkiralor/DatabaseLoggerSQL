import datetime as dt
import sqlite3
import smtplib
import requests
import multiprocessing
import json

import sys

sys.path.append('/home/prithoo/Coding/DatabaseLoggerSQL')

with open ('CONFIG.json') as fp:
    config = json.load(fp)


class Events():
                event_id = None
                message = None
                datetime = None

                def __init__(self, message:str):
                    self.message = message
                    self.datetime = dt.datetime.now()
                def __repr__(self):
                    return "<Event('%s','%s')>" % (self.message, self.datetime)


class EventLogger():
    TABLE_NAME = None

    def __init__(self, table_name):
        self.TABLE_NAME = table_name
        db = sqlite3.connect("LOGS.db")
        cur = db.cursor()

        create_query = f'CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT, msg VARCHAR(255), date DATETIME)'

        cur.execute(create_query)


        self.slack_notifier = SlackNotifier()
        self.email_notifier = EmailNotifier()

        return True

    
    def push_to_table(self, msg:str, slack = False, email = False):
        
        event = Events(msg)
        
        db = sqlite3.connect("LOGS.db")
        cur = db.cursor()

        insert_query = f"INSERT INTO {self.TABLE_NAME} (msg, date) VALUES ('{event.message}', '{event.datetime}')"
        
        cur.execute(insert_query)
        
        if slack == True:
            slack_process = multiprocessing.Process(target=self.slack_notifier.notification, args=(msg, ))
            slack_process.start()

        if email == True:
            try:
                email_process = multiprocessing.Process(target=self.email_notifier.mail_notifier, args=(msg, ))
                email_process.start()
            except Exception as er:
                print(er)

        db.commit()

        cur.close()
        db.close()

        return {'push_to_table': True}


class SlackNotifier():

    def __init__(self):
        self.slack_url = config["slack"]['webhook']
        self.app_name = config["slack"]["app_name"]
            
    def notification(self, msg:str):
        
        message = f"Notification from {self.app_name}: {msg}"

        payload = {"text": message}
        response = requests.post(self.slack_url, json = payload)

        response_data = response.text

        return response_data
        # print(response_data)

    
class EmailNotifier():
    def __init__(self):
        self.mail_server = config['email']['mail_server']
        self.server_port = int(config['email']['server_port'])
        
        self.server = smtplib.SMTP_SSL(self.mail_server, self.server_port)
        
        self.serveruid = config['email']['username']
        self.server_app_password = config['email']['password']
        self.app_name = config['email']['app_name']

        
    
    def mail_notifier(self, msg:str):
        #message = f"Notification from {self.app_name}: {msg}"
        message = msg

        try:
            self.server.login(self.serveruid, self.server_app_password)
            
            self.server.sendmail(
                config['email']['sender_email'],
                config['email']['recipient_email'],
                message
            )

            return {'email':True}
        except Exception as e:
            print({'Error':f'{e}; Could not send email.'}) 
                
            self.server.quit()

            return {'email':False, 'error': str(e)}


if __name__ == "__main__":
    e1 = EventLogger('new_new_table')
    e1.push_to_table('New new second mail!', slack = True, email = True)

    e2 = EventLogger('new_old_table')
    e2.push_to_table('Hello World.', slack = True, )