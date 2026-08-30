import re
import datetime

def parse_auth_log(line):
    pattern = r'(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<host>\S+)\s+(?P<process>\w+)\[(?P<pid>\d+)\]:\s+(?P<message>.*)'
    m = re.match(pattern, line)
    if not m:
        return None

    data = m.groupdict()
    year = datetime.datetime.now().year
    month_map = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,
                 'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    month = month_map.get(data['month'], 1)
    day = int(data['day'])
    hour, minute, second = map(int, data['time'].split(':'))
    try:
        timestamp = datetime.datetime(year, month, day, hour, minute, second)
    except:
        timestamp = None

    message = data['message']
    event = 'other'
    user = None
    ip = None

    if 'Failed password' in message:
        event = 'failed_login'
        user_match = re.search(r'for (invalid user )?(?P<user>\S+)', message)
        if user_match:
            user = user_match.group('user')
        ip_match = re.search(r'from (?P<ip>\d+\.\d+\.\d+\.\d+)', message)
        if ip_match:
            ip = ip_match.group('ip')
    elif 'Accepted password' in message or 'Accepted publickey' in message:
        event = 'successful_login'
        user_match = re.search(r'for (?P<user>\S+)', message)
        if user_match:
            user = user_match.group('user')
        ip_match = re.search(r'from (?P<ip>\d+\.\d+\.\d+\.\d+)', message)
        if ip_match:
            ip = ip_match.group('ip')
    elif 'Disconnected' in message:
        event = 'disconnect'

    return {'timestamp': timestamp, 'host': data['host'], 'event': event, 'user': user, 'ip': ip, 'raw': line.strip()}
