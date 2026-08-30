import pandas as pd
from parser import parse_auth_log

def analyze_log(filepath):
    events = []
    with open(filepath, 'r') as f:
        for line in f:
            parsed = parse_auth_log(line)
            if parsed:
                events.append(parsed)

    df = pd.DataFrame(events)
    if df.empty:
        return {}

    if 'timestamp' in df:
        df = df.dropna(subset=['timestamp'])

    total = len(df)
    failed = len(df[df['event'] == 'failed_login']) if 'event' in df else 0
    success = len(df[df['event'] == 'successful_login']) if 'event' in df else 0
    unique_ips = df['ip'].nunique() if 'ip' in df else 0

    if 'ip' in df and 'event' in df:
        top_offenders = df[df['event'] == 'failed_login']['ip'].value_counts().head(10).to_dict()
    else:
        top_offenders = {}

    brute_force_ips = []
    if 'ip' in df and 'timestamp' in df and 'event' in df:
        df_sorted = df[df['event'] == 'failed_login'].sort_values('timestamp')
        for ip, group in df_sorted.groupby('ip'):
            if len(group) < 5:
                continue
            if group['timestamp'].notna().any():
                max_time = group['timestamp'].max()
                min_time = group['timestamp'].min()
                if (max_time - min_time).seconds <= 300:
                    brute_force_ips.append(ip)

    if 'timestamp' in df:
        df['hour'] = df['timestamp'].dt.floor('h')
        timeline = df.groupby('hour').size().to_dict()
    else:
        timeline = {}

    return {
        'total_events': total,
        'failed_logins': failed,
        'successful_logins': success,
        'unique_ips': unique_ips,
        'top_offenders': top_offenders,
        'brute_force_ips': brute_force_ips,
        'timeline': timeline,
        'events_df': df
    }
