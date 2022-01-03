pytest --alluredir=../AllureReports unit_tests/test_01.py -v
python unit_tests/allure_config.py
allure serve reports
# PID=$!
# sleep 5
# kill -INT $PID