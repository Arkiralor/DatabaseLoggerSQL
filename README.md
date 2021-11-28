# DATABASE BASED LOGGER

<p>
A source-code logger that takes a snapshot of the machine's software and hardware state and saves
a textual description (user-defined) of the state to a database called 'LOGS.db', which is a 
sqlite database (*.db) file.
</p>

### How to use:
<p>
Simply define an event and call the event's 'push_to_table' method in case of eny exceptions occuring at runtime.
</p>

#### Example of Usage:

From [Example.PY](https://github.com/Arkiralor/DatabaseLoggerSQL/blob/main/example.py) in repository:


            '''
            Let's try to devide by zero.
            '''
            event = EventLogger('error_table')
            try:
                print(3/0)
            except Exception as err:
                event.push_to_table(f'Error: {err}', slack=True, email=False, hw_monitor=True)

### Classes:
<p>
A brief description of all the classes declared and defined in the package:
</p>

1. #### Events:
    
    A class to record the details of a particular event as defined by the user.
2. #### EventLogger:
    
    A class to initiate the Log tables in the database and contains instances of all the other classes and their methods.
3. #### SlackNotifier:
    
    A class to initialize the SlackApp connection and to send a notification to a particular channel in the app whenever called to do so.
4. #### EmailNotifier:
    
    A class to initialize an email server connection and to send an email notofication to the defined recipient whenever called to do so.
5. #### Monitor:
    
    A class to initialize the HW-Monitor and to store system HW snapshots in a DICT format to the db whenever called to do so.

### Methods:
<p>
A brief decription of the methods that can be called by the package:
</p>

1. #### EventLogger.push_to_table(msg: str, slack:bool=False, email:bool=False,  hw_monitor:bool=False):
    
    <p>
    The method to be used to push the current event description into the database table as defined by the user when initializing the class.

    If any of the following: slack, email or hw_monitor are set as 'True', the corresponding notification or db-commit method is called. </p>
2. #### SlackNotifier.notification(msg:str):
    
    <p>
    The method called when 'slack' is set to 'True' in method#1 above. It passes the 'msg' string included as the argument to an incoming webhook to a defined slack channel and posts it there as a message. </p>
3. #### EmailNotifier.mail_notifier(msg: str):
    
    <p>
    The method called when 'email' is set to 'True' in method#1 above. It passes the 'msg' string included as the argument to an outgoing request to a defined email server and id and posts it there as an email. </p>
4. #### Monitor.monitor(msg: str, process_id: int = os.getpid(), date: dt.datetime = dt.datetime.now()):
    
    <p>
    The method called when 'hw_monitor' is set to 'True' in method#1 above. It passes the 'msg' string, the malfunctioning module's current process id and the malfunctioning module's timestamp to a data-set and concatenates it with the malfunctioning module's CPU and Memory consumption snapshot and saves the data to the 'hw_logs' table in the concerned database. </p>

### Contributors:

1. [Prithoo Medhi](https://github.com/Prithoo-Medhi) & [Arkiralor](https://github.com/Arkiralor)
2. [Sivaranjan Goswami](https://github.com/sivgos)