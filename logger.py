'''
This is the main module of the library and deals with the events and the logging of events and
the event's data to the database.

This module also calls all the other modules/classes present in the library.

Therefore only this module needs to be imported from this library for the code to work.
'''
import datetime as dt
import sqlite3
from hw_monitor import Monitor
from slacknotifier import SlackNotifier
from emailnotifier import EmailNotifier
import multiprocessing
import os
from dotenv import load_dotenv
import sys

'''
Unused imports:
'''
# import smtplib
# import requests

# import psutil as ps
# import json
# from os import path


sys.path.append('/home/prithoo/Coding/DatabaseLoggerSQL')


load_dotenv()


class Events():
    '''
    Class to contain event specific data of that needs to be commited to the database:
    '''
    event_id = None
    message: str = None
    process_id: int = None
    datetime: dt.datetime = None

    def __init__(self, message: str, process_id: int):
        '''
        Method to store event-specific data to the class-variables:
        '''
        self.message = message
        self.process_id = process_id
        self.datetime = dt.datetime.now()

    def __repr__(self):
        '''
        Representation method to print the class-variables, in case of requirement:
        '''
        return "<Event('%s','%s','%s')>" % (self.message, self.process_id, self.datetime)


class EventLogger():
    '''
    Class to contain methods and data relating to what needs to be logged (committed) to the database:
    '''
    TABLE_NAME = None

    def __init__(self, table_name):
        '''
        Method o initialize the class along with the required table in the database:
        '''
        self.TABLE_NAME = table_name
        db = sqlite3.connect("LOGS.db")
        cur = db.cursor()

        create_query = f'CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT, msg VARCHAR(255), date DATETIME)'

        cur.execute(create_query)
        db.commit()

        cur.close()
        db.close()

        self.slack_notifier = SlackNotifier()
        self.email_notifier = EmailNotifier()
        self.monitor = Monitor()

    def push_to_table(self, msg: str, slack=False, email=False, hw_monitor=False):
        '''
        Method to push and commit the event-specific data to the database:
        '''
        event = Events(msg, process_id=os.getpid())

        db = sqlite3.connect("LOGS.db")
        cur = db.cursor()

        insert_query = f"INSERT INTO {self.TABLE_NAME} (msg, date) VALUES ('{event.message}', '{event.datetime}')"

        cur.execute(insert_query)

        db.commit()

        cur.close()
        db.close()

        if slack == True:
            slack_process = multiprocessing.Process(
                target=self.slack_notifier.notification, args=(msg, ))
            slack_process.start()
            # self.slack_notifier.notification(msg)

        if email == True:
            try:
                email_process = multiprocessing.Process(
                    target=self.email_notifier.mail_notifier, args=(msg, ))
                email_process.start()
                # self.email_notifier.mail_notifier(msg)
            except Exception as er:
                print(er)

        if hw_monitor == True:
            try:
                hw_process = multiprocessing.Process(
                    target=self.monitor.monitor, args=(msg, event.process_id, event.datetime))
                hw_process.start()
                # self.monitor.monitor(
                #     msg, process_id=event.process_id, date=event.datetime)
            except Exception as er:
                print(er)

        return {'push_to_table': True}


# class SlackNotifier():

#     def __init__(self):
#         self.slack_url = os.environ.get('webhook')
#         self.app_name = os.environ.get('slack_app_name')

#     def notification(self, msg: str):

#         message = f"{self.app_name}: {msg}"

#         payload = {"text": message}
#         response = requests.post(self.slack_url, json=payload)

#         response_data = response.text

#         print(response_data)
#         # return response_data


# class EmailNotifier():
#     def __init__(self):
#         self.mail_server = os.environ.get('mail_server')
#         self.server_port = int(os.environ.get('server_port'))

#         self.server = smtplib.SMTP_SSL(self.mail_server, self.server_port)

#         self.serveruid = os.environ.get('username')
#         self.server_app_password = os.environ.get('password')
#         self.app_name = os.environ.get('email_app_name')

#     def mail_notifier(self, msg: str):

#         message = msg

#         try:
#             self.server.login(self.serveruid, self.server_app_password)

#             self.server.sendmail(
#                 os.environ.get('sender_email'),
#                 os.environ.get('recipient_email'),
#                 message
#             )

#             self.server.quit()

#             # print({'email': True})
#             # return {'email': True}
#         except Exception as e:
#             print({'Error': f'{e}; Could not send email.'})

#             self.server.quit()

#             # print({'email': False, 'error': str(e)})
#             # return {'email': False, 'error': str(e)}


# class Monitor():
#     '''
#     Class for all monitoring activities:
#     '''
#     TABLE_NAME: str = 'hw_logs'

#     def __init__(self):
#         # self.TABLE_NAME = table_name
#         db = sqlite3.connect("LOGS.db")
#         cur = db.cursor()

#         create_query = f'CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT, task VARCHAR, pid INTEGER, cpu_times VARCHAR, cpu_usage VARCHAR, memory VARCHAR, mem_use VARCHAR, read_count INTEGER, write_count INTEGER, date DATETIME)'

#         cur.execute(create_query)

#         cpu, cpu_perc = ps.cpu_freq(), ps.cpu_percent()
#         mem, swap_mem = ps.virtual_memory(), ps.swap_memory()

#         log_dict = {
#             "cpu_frequency": cpu,
#             "cpu_usage_percentage": cpu_perc,
#             "virtual_memory_percentage": mem,
#             "swap_memory_used": swap_mem
#         }

#         with open('config/config.json', 'wt')as conf_file:
#             conf_file.write(json.dumps(log_dict))
#             conf_file.write("\n")

#     def monitor(self, msg: str, process_id: int = os.getpid(), date: dt.datetime = dt.datetime.now()):
#         '''
#         Method to write hardware logs to db:
#         '''
#         try:
#             targ = ps.Process(process_id)

#             targ_pid = targ.pid
#             targ_cpu_times = targ.cpu_times().user + targ.cpu_times().system
#             targ_cpu_usage = targ.cpu_percent()
#             targ_mem = targ.memory_info().rss
#             targ_mem_use = targ.memory_percent()
#             targ_read_count = targ.io_counters().read_count
#             targ_write_count = targ.io_counters().write_count

#             # print(targ_pid)
#             # print(targ_cpu_times)
#             # print(targ_cpu_usage)
#             # print(targ_mem)
#             # print(targ_mem_use)
#             # print(targ_read_count)
#             # print(targ_write_count)

#             db = sqlite3.connect("LOGS.db")
#             cur = db.cursor()

#             insert_query = f"INSERT INTO {self.TABLE_NAME} (task, pid , cpu_times , cpu_usage , memory , mem_use , read_count , write_count , date) VALUES ('{msg}', '{targ_pid}', '{targ_cpu_times}', '{targ_cpu_usage}', '{targ_mem}', '{targ_mem_use}', '{targ_read_count}', '{targ_write_count}', '{date}' )"

#             cur.execute(insert_query)
#             db.commit()
#             cur.close()
#             db.close()
#         except Exception as err:
#             print(f'Error: {str(err)}')


if __name__ == "__main__":
    # e1 = EventLogger('new_new_table')
    # e1.push_to_table('New new second mail!', slack=True, email=True)

    e2 = EventLogger('error_table')
    try:
        print(3/0)
    except Exception as err:
        e2.push_to_table(f'Error: {err}', slack=True,
                         email=False, hw_monitor=True)
