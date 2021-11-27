from dotenv import load_dotenv
import os
import psutil as ps

load_dotenv()

# slack = os.environ.get('slack_app_name')
# print(slack)

a = ps.swap_memory()
print(type(a))
print(a)