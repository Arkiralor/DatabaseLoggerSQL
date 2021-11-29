from sqlite3.dbapi2 import Date
from logger import EventLogger
import datetime

if __name__ == "__main__":
    e2 = EventLogger(table_name='error_table')
    try:
        print(3/0)
    except Exception as err:
        e2.push_to_table(f'Error: {err} at {datetime.datetime.now()}', hw_monitor=True)
        # raise Exception(err)
