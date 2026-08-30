import random
import datetime

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def generate_log_line(timestamp, host='testhost', ip=None, event='failed', user=None):
    if user is None:
        user = random.choice(['root','admin','user1','test','guest'])
    if ip is None:
        ip = random_ip()
    if event == 'failed':
        msg = f"Failed password for invalid user {user} from {ip} port {random.randint(1000,65535)}"
    elif event == 'success':
        msg = f"Accepted password for {user} from {ip} port {random.randint(1000,65535)}"
    else:
        msg = "Disconnected from " + ip
    return f"{timestamp.strftime('%b %d %H:%M:%S')} {host} sshd[{random.randint(1000,9999)}]: {msg}"

# Generate 1000 lines
with open('sample.log', 'w') as f:
    base = datetime.datetime.now() - datetime.timedelta(days=1)
    for i in range(1000):
        dt = base + datetime.timedelta(seconds=random.randint(0, 86400))
        event = random.choices(['failed','success','other'], weights=[0.7,0.2,0.1])[0]
        if event == 'failed':
            # 10% chance of brute-force (many from same IP)
            if random.random() < 0.1:
                ip = '192.168.1.100'  # same IP
            else:
                ip = random_ip()
        else:
            ip = random_ip()
        line = generate_log_line(dt, ip=ip, event=event)
        f.write(line + '\n')
