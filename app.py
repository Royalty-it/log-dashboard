from flask import Flask, render_template
from analyzer import analyze_log
import plotly.express as px
import pandas as pd

app = Flask(__name__)

@app.route('/')
def dashboard():
    data = analyze_log('/home/ankoo/Desktop/log-dashboard/sample.log')
    df = data.get('events_df', pd.DataFrame())

    total = len(df)
    failed = len(df[df['event'] == 'failed_login']) if 'event' in df else 0
    success = len(df[df['event'] == 'successful_login']) if 'event' in df else 0
    unique_ips = df['ip'].nunique() if 'ip' in df else 0

    # Pie chart
    if not df.empty:
        event_counts = df['event'].value_counts().reset_index()
        event_counts.columns = ['event', 'count']
        fig_pie = px.pie(event_counts, values='count', names='event', title='Event Distribution')
        pie_html = fig_pie.to_html(full_html=False)
    else:
        pie_html = ""

    # Bar chart (top offenders)
    if 'ip' in df and not df.empty:
        offenders = df[df['event'] == 'failed_login']['ip'].value_counts().head(10).reset_index()
        if not offenders.empty:
            offenders.columns = ['IP', 'Failed Attempts']
            fig_bar = px.bar(offenders, x='IP', y='Failed Attempts', title='Top Offending IPs')
            bar_html = fig_bar.to_html(full_html=False)
        else:
            bar_html = ""
    else:
        bar_html = ""

    # Line chart (timeline)
    if 'timestamp' in df and not df.empty:
        df['hour'] = df['timestamp'].dt.floor('h')
        timeline = df.groupby('hour').size().reset_index(name='Events')
        fig_line = px.line(timeline, x='hour', y='Events', title='Events Over Time')
        line_html = fig_line.to_html(full_html=False)
    else:
        line_html = ""

    # Table
    table_data = df[['timestamp', 'event', 'ip', 'user']].head(100).to_dict(orient='records') if not df.empty else []

    return render_template('dashboard.html',
                           total_events=total,
                           failed_logins=failed,
                           successful_logins=success,
                           unique_ips=unique_ips,
                           table_data=table_data,
                           pie_html=pie_html,
                           bar_html=bar_html,
                           line_html=line_html)

if __name__ == '__main__':
    app.run(debug=True)
