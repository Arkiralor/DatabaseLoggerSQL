'''
This module deals with the Slack notification abilities of the library.
'''
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class SlackNotifier():
    '''
    Class to contain methods and data to send notifications via Slack webhooks:
    '''
    def __init__(self):
        '''
        Method to initialize slack webhook service:
        '''
        self.slack_url = os.environ.get('webhook')
        self.app_name = os.environ.get('slack_app_name')

    def notification(self, msg: str):
        '''
        Method to send notifications via Slack webhooks:
        '''
        message = f"{self.app_name}: {msg}"

        payload = {"text": message}
        response = requests.post(self.slack_url, json=payload)

        # response_data = response.text

        # print(response.text)
        # return response
