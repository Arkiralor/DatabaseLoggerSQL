from notifier import EventLogger

if __name__ == "__main__":
    e1 = EventLogger('Example_Table_01')
    e1.push_to_table('New new second mail!', slack = True, email = True)

    e2 = EventLogger('Example_Table_02')
    e2.push_to_table('Hello World.', slack = True, )
    e2.push_to_table('Sent from object 2!', slack = True, email = True)