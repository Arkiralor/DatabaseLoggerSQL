import sqlite3
import psutil as ps
import json
import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv()


class Monitor():
    '''
    Class for all monitoring activities:
    '''
    TABLE_NAME: str = 'hw_logs'

    def __init__(self):
        # self.TABLE_NAME = table_name
        db = sqlite3.connect("LOGS.db")
        cur = db.cursor()

        create_query = f'CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT, task VARCHAR, pid INTEGER, cpu_times VARCHAR, cpu_usage VARCHAR, memory VARCHAR, mem_use VARCHAR, read_count INTEGER, write_count INTEGER, date DATETIME)'

        cur.execute(create_query)

        cpu, cpu_perc = ps.cpu_freq(), ps.cpu_percent()
        mem, swap_mem = ps.virtual_memory(), ps.swap_memory()

        log_dict = {
            "cpu_frequency": cpu,
            "cpu_usage_percentage": cpu_perc,
            "virtual_memory_percentage": mem,
            "swap_memory_used": swap_mem
        }

        with open('config/config.json', 'wt')as conf_file:
            conf_file.write(json.dumps(log_dict))
            conf_file.write("\n")

    def monitor(self, msg: str, process_id: int = os.getpid(), date: dt.datetime = dt.datetime.now()):
        '''
        Method to write hardware logs to db:
        '''
        try:
            targ = ps.Process(process_id)

            targ_pid = targ.pid
            targ_cpu_times = targ.cpu_times().user + targ.cpu_times().system
            targ_cpu_usage = targ.cpu_percent()
            targ_mem = targ.memory_info().rss
            targ_mem_use = targ.memory_percent()
            targ_read_count = targ.io_counters().read_count
            targ_write_count = targ.io_counters().write_count

            # print(targ_pid)
            # print(targ_cpu_times)
            # print(targ_cpu_usage)
            # print(targ_mem)
            # print(targ_mem_use)
            # print(targ_read_count)
            # print(targ_write_count)

            db = sqlite3.connect("LOGS.db")
            cur = db.cursor()

            insert_query = f"INSERT INTO {self.TABLE_NAME} (task, pid , cpu_times , cpu_usage , memory , mem_use , read_count , write_count , date) VALUES ('{msg}', '{targ_pid}', '{targ_cpu_times}', '{targ_cpu_usage}', '{targ_mem}', '{targ_mem_use}', '{targ_read_count}', '{targ_write_count}', '{date}' )"

            cur.execute(insert_query)
            db.commit()
            cur.close()
            db.close()
        except Exception as err:
            print(f'Error: {str(err)}')
