pytest --alluredir=../reports test_01.py -v
python allure_config.py
allure serve reports
# PID=$!
# sleep 5
# kill -INT $PID