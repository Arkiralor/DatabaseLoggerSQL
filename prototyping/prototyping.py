from dotenv import load_dotenv
import os
import psutil as ps

load_dotenv()

# slack = os.environ.get('slack_app_name')
# print(slack)

targ = ps.Process(os.getpid())

targ_pid = targ.pid
# targ_cpu_times = targ.cpu_times().user + targ.cpu_times().system
print(type(targ_pid))
print(targ_pid)