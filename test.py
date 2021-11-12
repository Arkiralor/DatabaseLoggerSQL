from dotenv import load_dotenv
import os

load_dotenv()

slack = os.environ.get('slack_app_name')
print(slack)