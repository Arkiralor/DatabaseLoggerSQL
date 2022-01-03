import unittest
import sys
import pytest
import allure

# sys.path.append('/home/prithoo/Coding/DatabaseLoggerSQL')
# from ..notifier import EventLogger, SlackNotifier, EmailNotifier, Monitor
from ..logger import EventLogger
from ..emailnotifier import EmailNotifier
from ..slacknotifier import SlackNotifier
from ..hw_monitor import Monitor


class DatabaseTest(unittest.TestCase):

    
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ptt(self):
        msg:str = 'this is from unit-test.'
        tablename:str = 'plain_table'
        
        event_01 = EventLogger(tablename)
        passed_test:bool = event_01.push_to_table(msg)

        self.assertTrue(passed_test == {'push_to_table': True})


    @allure.severity(allure.severity_level.NORMAL)
    def test_ptt_slack(self):
        msg:str = 'this is from unit-test with slack.'
        tablename:str = 'plain_table_slack'
        
        event_01 = EventLogger(tablename)
        passed_test:bool = event_01.push_to_table(msg, slack=True, email=False)

        self.assertTrue(passed_test == {'push_to_table': True})

    
    @allure.severity(allure.severity_level.NORMAL)
    def test_ptt_email(self):
        msg:str = 'this is from unit-test with email.'
        tablename:str = 'plain_table_email'
        
        event_01 = EventLogger(tablename)
        passed_test:bool = event_01.push_to_table(msg, slack=False, email=True)

        self.assertTrue(passed_test == {'push_to_table': True})


    @allure.severity(allure.severity_level.TRIVIAL)
    def test_ptt_slack_and_email(self):
        msg:str = 'this is from unit-test with slack and email.'
        tablename:str = 'plain_table_slack_email'
        
        event_01 = EventLogger(tablename)
        passed_test:bool = event_01.push_to_table(msg, slack=True, email=True)

        self.assertTrue(passed_test == {'push_to_table': True})

    @allure.severity(allure.severity_level.NORMAL)
    def test_ptt_hwlogs(self):
        msg:str = 'this is from unit-test with hardware logs.'
        tablename:str = 'hw_log_test'
        
        event_01 = EventLogger(tablename)
        passed_test:bool = event_01.push_to_table(msg, slack=False, email=False, hw_monitor=True)

        self.assertTrue(passed_test == {'push_to_table': True})

    #This is meant to fail:
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tablename(self):
        tablename:str = 'entered_table'
        event_01 = EventLogger(tablename)

        self.assertRegex(event_01.TABLE_NAME, 'random_table')


class SlackTest(unittest.TestCase):
    
    @allure.severity(allure.severity_level.MINOR)
    def test_slack_notif(self):
        msg:str = 'this is from slack-test.'
        
        slack_01 = SlackNotifier()
        passed_slack:str = slack_01.notification(msg)

        self.assertTrue(passed_slack == 'ok')


class EmailTest(unittest.TestCase):


    @allure.severity(allure.severity_level.MINOR)
    def test_email(self):
        msg:str = 'this is from email-test.'
        
        email_01 = EmailNotifier()
        passed_email = email_01.mail_notifier(msg)

        self.assertTrue(passed_email == {'email': True})


if __name__ == "__main__":

    unittest.main()