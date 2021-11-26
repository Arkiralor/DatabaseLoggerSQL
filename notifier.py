import datetime as dt
import sqlite3
import smtplib
import requests
import multiprocessing
import psutil as ps
import json
import os
from os import path
from dotenv import load_dotenv
import sys

sys.path.append('/home/prithoo/Coding/DatabaseLoggerSQL')


load_dotenv()


class Events():
            event_id = None
            message = None
            datetime = None

            def __init__(self, message: str):
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
        self.monitor = Monitor('hw_logs')

    def push_to_table(self, msg: str, slack=False, email= False, hw_monitor = False):

        event = Events(msg)

        db = sqlite3.connect("LOGS.db")
        cur = db.cursor()

        insert_query = f"INSERT INTO {self.TABLE_NAME} (msg, date) VALUES ('{event.message}', '{event.datetime}')"

        cur.execute(insert_query)

        if slack == True:
            # slack_process = multiprocessing.Process(
            #     target=self.slack_notifier.notification, args=(msg, ))
            # slack_process.start()
            self.slack_notifier.notification(msg)

        if email == True:
            try:
                # email_process = multiprocessing.Process(
                #     target=self.email_notifier.mail_notifier, args=(msg, ))
                # email_process.start()
                self.email_notifier.mail_notifier(msg)
            except Exception as er:
                print(er)

        if hw_monitor == True:
            try:
                # hw_process = multiprocessing.Process(
                #     target=self.monitor.monitor, args=(msg,))
                # hw_process.start()
                self.monitor.monitor(msg)
            except Exception as er:
                print(er)

        db.commit()

        cur.close()
        db.close()

        return {'push_to_table': True}


class SlackNotifier():

    def __init__(self):
        self.slack_url = os.environ.get('webhook')
        self.app_name = os.environ.get('slack_app_name')

    def notification(self, msg: str):

        message = f"Notification from {self.app_name}: {msg}"

        payload = {"text": message}
        response = requests.post(self.slack_url, json=payload)

        response_data = response.text

        print(response_data)
        return response_data


class EmailNotifier():
    def __init__(self):
        self.mail_server = os.environ.get('mail_server')
        self.server_port = int(os.environ.get('server_port'))

        self.server = smtplib.SMTP_SSL(self.mail_server, self.server_port)

        self.serveruid = os.environ.get('username')
        self.server_app_password = os.environ.get('password')
        self.app_name = os.environ.get('email_app_name')

    def mail_notifier(self, msg: str):

        message = msg

        try:
            self.server.login(self.serveruid, self.server_app_password)

            self.server.sendmail(
                os.environ.get('sender_email'),
                os.environ.get('recipient_email'),
                message
            )

            self.server.quit()

            # print({'email': True})
            # return {'email': True}
        except Exception as e:
            print({'Error': f'{e}; Could not send email.'})

            self.server.quit()

            # print({'email': False, 'error': str(e)})
            # return {'email': False, 'error': str(e)}


class Monitor():
    '''
    Class for all monitoring activities:
    '''
    TABLE_NAME: path = None

    def __init__(self, table_name):
        self.TABLE_NAME = table_name
        db = sqlite3.connect("LOGS.db")
        cur = db.cursor()

        create_query = f'CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT, task VARCHAR(1024), date DATETIME)'

        cur.execute(create_query)

    def monitor(self, msg: str):
        '''
        Method to write hardware logs to db:
        '''
        cpu, cpu_perc = ps.cpu_freq(), ps.cpu_percent()
        mem, swap_mem = ps.virtual_memory(), ps.swap_memory()

        log_dict = {
            "Task": msg,
            "CPU Frequency": str(cpu),
            "CPU Usage": str(cpu_perc),
            "Memory Usage": str(mem),
            "Swap File": str(swap_mem)
        }

        db = sqlite3.connect("LOGS.db")
        cur = db.cursor()

        insert_query = f"INSERT INTO {self.TABLE_NAME} (task, date) VALUES ('{json.dumps(log_dict)}', '{dt.datetime.now()}')"

        cur.execute(insert_query)



if __name__ == "__main__":
    e1 = EventLogger('new_new_table')
    e1.push_to_table('New new second mail!', slack=True, email=True)

    e2 = EventLogger('new_old_table')
    e2.push_to_table('Hello World.', slack=True, email=False, hw_monitor=True )
