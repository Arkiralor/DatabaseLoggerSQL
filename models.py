import datetime as dt
import sqlite3
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, inspect
from sqlalchemy.orm import sessionmaker, mapper

from sqlalchemy.ext.declarative import declarative_base
import datetime as dt
import json


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
    
    def push_to_table(self, msg:str):
        
        event = Events(msg)
        
        db = sqlite3.connect("LOGS.db")
        cur = db.cursor()

        insert_query = f"INSERT INTO {self.TABLE_NAME} (msg, date) VALUES ('{event.message}', '{event.datetime}')"
        cur.execute(insert_query)
        db.commit()

        cur.close()
        db.close()

if __name__ == "__main__":
    e1 = EventLogger('new_new_table')
    e1.push_to_table('old')

    e2 = EventLogger('new_old_table')
    e2.push_to_table('Hello World.')