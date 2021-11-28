from logger import EventLogger

if __name__ == "__main__":
    # e1 = EventLogger('Example_Table_01')
    # e1.push_to_table('New new second mail!', slack = True, email = True)

    e2 = EventLogger('error_table')
    try:
        print(3/0)
    except Exception as err:
        e2.push_to_table(f'Error: {err}', slack=True, email=False, hw_monitor=True)