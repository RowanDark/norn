from flask import Flask, render_template_string
import schedule
import time
from src.collector import collect_logs
from src.analyzer import normalize_logs, detect_anomalies
from src.storage import store_alerts, send_alerts

app = Flask(__name__)

def job():
    logs = collect_logs('sample_logs.csv')
    normalized = normalize_logs(logs)
    alerts = detect_anomalies(normalized)
    store_alerts(alerts)
    send_alerts(alerts)

     for _, alert in alerts.iterrows():
        execute_playbook(alert)
    print("Job completed with SOAR automation.")

@app.route('/')
def dashboard():
    # Simple HTML dashboard
    return render_template_string("""
    <h1>VibeSIEM Dashboard</h1>
    <p>Check console for alerts. Expand me!</p>
    """)

if __name__ == '__main__':
    schedule.every(10).seconds.do(job)  # Run every 10s for demo
    while True:
        schedule.run_pending()
        time.sleep(1)
    # app.run(debug=True)  # Uncomment for web server
