# DATABASE BASED LOGGER

<p>
A source-code logger that takes a snapshot of the machine's software and hardware state and saves
a textual description (user-defined) of the state to a database called 'LOGS.db', which is a 
sqlite database (*.db) file.
</p>

### Classes:
<p>
A brief description of all the classes declared and defined in the package:
</p>

#### 1. Events:
    A class to record the details of a particular event as defined by the user.
#### 2. EventLogger:
    A class to initiate the Log tables in the database and contains instances of all the other classes and their methods.
#### 3. SlackNotifier:
    A class to initialize the SlackApp connection and to send a notification to a particular channel in the app whenever called to do so.
#### 4. EmailNotifier:
    A class to initialize an email server connection and to send an email notofication to the defined recipient whenever called to do so.
#### 5. Monitor:
    A class to initialize the HW-Monitor and to store system HW snapshots in a DICT format to the db whenever called to do so.

### Methods:
<p>
A brief decription of the methods that can be called by the package:
</p>

1. EventLogger.push_to_table(msg: str, slack:bool=False, email:bool=False,  hw_monitor:bool=False):
    
    The method to be used to push the current event description into the database table as defined by the user when initializing the class.

    If any of the following: slack, email or hw_monitor are set as 'True', the corresponding notification or db-commit method is called.
2. SlackNotifier.notification(msg:str):

    The method called when 'slack' is set to 'True' in method#1 above. It passes the 'msg' string included as the argument to an incoming webhook to a defined slack channel and posts it there as a message.
3.
4.
5.