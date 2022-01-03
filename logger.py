'''
This is the main module of the library and deals with the events and the logging of events and
the event's data to the database.

This module also calls all the other modules/classes present in the library.

Therefore only this module needs to be imported from this library for the code to work.
'''
import datetime as dt
import sqlite3
from .hw_monitor import Monitor
from .slacknotifier import SlackNotifier
from .emailnotifier import EmailNotifier
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


# sys.path.append('/home/prithoo/Coding/DatabaseLoggerSQL')


load_dotenv()


class Events():
    '''
    Class to contain event specific data of what needs to be commited to the database:
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
        return "<Event(Message: '%s', Process_ID: '%s', Date of Creation: '%s')>" % (self.message, self.process_id, self.datetime)


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

        try:
            create_query = f'CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT, msg VARCHAR, date DATETIME)'
            cur.execute(create_query)
            db.commit()

            cur.close()
            db.close()
        except Exception as err:
            print(f'Error in Log_init: {err}')

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

        try:
            insert_query = f"INSERT INTO {self.TABLE_NAME} (msg, date) VALUES ('{event.message}', '{event.datetime}')"
            cur.execute(insert_query)
            db.commit()

            cur.close()
            db.close()
        except Exception as err:
            # print(f'Error: {err}')
            event.message = err
            insert_query = f"INSERT INTO {self.TABLE_NAME} (msg, date) VALUES ('LOGGER Error: {event.message}', '{event.datetime}')"
            cur.execute(insert_query)
            db.commit()

            cur.close()
            db.close()

        if slack == True:
            try:
                slack_process = multiprocessing.Process(
                    target=self.slack_notifier.notification, args=(msg, ))
                slack_process.start()
            except Exception as er:
                print(f'Error in slack_notifier(): {er}')

        if email == True:
            try:
                email_process = multiprocessing.Process(
                    target=self.email_notifier.mail_notifier, args=(msg, ))
                email_process.start()
            except Exception as er:
                print(f'Error in email_notifier(): {er}')

        if hw_monitor == True:
            try:
                hw_process = multiprocessing.Process(
                    target=self.monitor.monitor, args=(msg, event.process_id, event.datetime))
                hw_process.start()
                # self.monitor.monitor(
                #     msg, process_id=event.process_id, date=event.datetime)
            except Exception as er:
                print(f'Error in hw_monitor(): {er}')

        return {'push_to_table': True}

if __name__ == "__main__":
    # e1 = EventLogger('new_new_table')
    # e1.push_to_table('New new second mail!', slack=True, email=True)

    e2 = EventLogger('error_table')
    try:
        print(3/0)
    except Exception as err:
        e2.push_to_table(f'Error: {err}', slack=True,
                         email=False, hw_monitor=True)
    # pass
