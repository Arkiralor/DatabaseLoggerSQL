import unittest
import sys

sys.path.append('/home/prithoo/Coding/DatabaseLoggerSQL')
from notifier import EventLogger, SlackNotifier, EmailNotifier

class DatabaseTest(unittest.TestCase):

    def test_ptt(self):
        msg:str = 'this is from unit-test.'
        tablename:str = 'plain_table'
        
        event_01 = EventLogger(tablename)
        passed_test:bool = event_01.push_to_table(msg)

        self.assertTrue(passed_test == {'push_to_table': True})



class SlackTest(unittest.TestCase):
    
    def test_slack_notif(self):
        msg:str = 'this is from slack-test.'
        
        slack_01 = SlackNotifier()
        passed_slack:str = slack_01.notification(msg)

        self.assertTrue(passed_slack == msg)


class EmailTest(unittest.TestCase):


    def test_email(self):
        msg:str = 'this is from email-test.'
        
        email_01 = EmailNotifier()
        passed_email = email_01.mail_notifier(msg)

        self.assertTrue(passed_email == {'email': True})


if __name__ == "__main__":
    unittest.main()