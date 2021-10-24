from models import EventLogger as el

if __name__ == "__main__":
    e1 = el('new_new_table')
    e1.push_to_table('old')
    e1.push_to_table('new')

    e2 = el('new_old_table')
    e2.push_to_table('Hello World.')