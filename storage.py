import sqlite3

def store_alerts(alerts, db_file='siem.db'):
    conn = sqlite3.connect(db_file)
    alerts.to_sql('alerts', conn, if_exists='append', index=False)
    conn.close()
    print(f"Stored {len(alerts)} alerts.")

# Basic alerting (expand to email/Slack)
def send_alerts(alerts):
    for _, alert in alerts.iterrows():
        print(f"ALERT: Anomalous event from {alert['source_ip']} at {alert['timestamp']}")
