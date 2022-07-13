
from cmath import exp
from redis import Redis
from flask import Flask, request
import json

app = Flask(__name__)
redis = Redis(host='redis', port=6379, decode_responses=True, charset="utf-8")

abnormal_ips_prefix = 'abnormal_IPs'
banned_ips_prefix = 'banned_IPs'
banned_count_rule = 3
banned_time = 3600 # 1h

@app.route('/')
def hello():
    count = redis.incr('hits')
    return 'Hello World! 该页面已被访问 {} 次。\n'.format(count)



@app.route('/info')
def info():
    abnormal_ips = getIPs(abnormal_ips_prefix)
    banned_ips = getIPs(banned_ips_prefix)

    return {'abnormal_ips': abnormal_ips,
            'banned_ips':banned_ips,
            'abnormal_ips_prefix':abnormal_ips_prefix,
            'banned_ips_prefix':banned_ips_prefix,
            'banned_count_rule':banned_count_rule,
            'banned_time':banned_time
            }
    

# 通过methods设置POST请求
@app.route('/detectionResult', methods=["POST"])
def detectionResult():

    # 接收处理json数据请求
    data = json.loads(request.data) # 将json字符串转为dict
    ips = data['abnormal_IPs']
    for ip in ips:
        
        if not str(ip).startswith('192.168.6') and not str(ip).startswith('0'):    
            print(ip)
            key = '{}:{}'.format(abnormal_ips_prefix,ip)
            expire_time_s = 20
            redis.incr(key)
            redis.expire(key,expire_time_s)

    processFireWall()
    return "OK"

def processFireWall():
    
    ips_keys = redis.keys('{}*'.format(abnormal_ips_prefix))
    for full_ip in ips_keys:
        count = redis.get(full_ip)
        ip = full_ip.split(':')[1]
        key = '{}:{}'.format(banned_ips_prefix,ip)
        if int(count) > banned_count_rule:
            redis.set(key,1)
            redis.expire(key,banned_time)

def getIPs(prefix,step=':'):
    res = redis.keys('{}*'.format(prefix))
    ips = []
    for item in res:
        ip = item.split(step)[1]
        ips.append(ip)

    return ips

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)