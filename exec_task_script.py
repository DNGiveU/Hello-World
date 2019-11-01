# _*_ encoding=utf-8 _*_
import requests
import datetime
import time
import json

"""
配置项: script_code、end_time
"""

# 运行脚本code
script_code = 'reportCrmUserResTypeDaily'
# 脚本结束日期, 如: datetime.date.today()
end_time = datetime.date(2019, 10, 31)
# 钉钉通知链接: 运行出错时通知
# 默认服务端监控:
ding_talk_url = 'your ding talk url'

"""
常量
"""

url_template = 'http://localhost/commdata/run.do?date=%s&scriptCode=%s'

# 开始时间
start_time = datetime.date(2019, 1, 25)

# 60 minutes
timeout_value = 1000 * 60 * 60

# retry count is 3
retry_count = 3


def send_ding_talk(error_msg):
    data = {
        'msgtype': 'text',
        'text': {
            'content': 'ibee任务脚本 [' + script_code + '] 执行出错: ' + error_msg
        },
        'at': {
            'atMobiles': [],
            'isAtAll': False
        }
    }
    response = requests.request(
        method='post',
        url=ding_talk_url,
        data=json.dumps(data),
        headers={'Content-type': 'application/json; charset=utf-8', 'Accept': 'application/json'}
    )
    response.close()


if __name__ == "__main__":
    try:
        while start_time.__lt__(end_time):
            dates = start_time.isoformat()
            url = url_template % (dates, script_code)

            # retry time = 3
            retry_times = 0
            while retry_times < retry_count:
                # timeout_value + retry_times * 30minutes
                timeouts = timeout_value + retry_times * 1000 * 60 * 30;
                retry_times = retry_times + 1
                try:
                    # timeout=(connect timeout, read timeout)
                    _response = requests.request('get', url, timeout=(timeouts, timeouts))
                    if _response.ok:
                        print("日期: " + dates + ", 响应码: " + _response.status_code + ", 响应内容: " + _response.text)
                        _response.close()
                        break
                    else:
                        print('WARN: '.dates)
                except ConnectionError as err:
                    print('ERROR: '.dates)

            # 时间值 day +1
            startTime = start_time.__add__(datetime.timedelta(1))

            # because the interface is executed asynchronous
            # sleep 15min = 15 * 60 = 900 seconds
            time.sleep(900)
    except (OSError, IOError, EnvironmentError, OverflowError, Exception) as err:
        # 发送钉钉通知
        send_ding_talk(err.__str__())
