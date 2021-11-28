import os
import requests

from dotenv import load_dotenv
import sys

load_dotenv()

class SlackNotifier():

    def __init__(self):
        self.slack_url = os.environ.get('webhook')
        self.app_name = os.environ.get('slack_app_name')

    def notification(self, msg: str):

        message = f"{self.app_name}: {msg}"

        payload = {"text": message}
        response = requests.post(self.slack_url, json=payload)

        response_data = response.text

        print(response_data)
        # return response_data