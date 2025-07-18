from flask import Flask, render_template_string, request
from flask_bootstrap import Bootstrap
import schedule
import time
from src.collector import collect_logs
from src.analyzer import normalize_logs, detect_anomalies
from src.storage import store_alerts, send_alerts

app = Flask(__name__)
Bootstrap(app)

def job():
    logs = collect_logs('sample_logs.csv')
    normalized = normalize_logs(logs)
    alerts = detect_anomalies(normalized)
    store_alerts(alerts)
    send_alerts(alerts)

     for _, alert in alerts.iterrows():
        execute_playbook(alert)
    print("Job completed with SOAR automation.")
    recent_alerts = alerts.to_dict('records')[:10]

@app.route('/', methods=['GET', 'POST'])
def dashboard():

      selected_theme = request.form.get('theme', 'blue-black')  # Default theme
    
    themes = {
        'blue-black': 'body { background: black; color: white; } table { border-color: blue; } th { background: navy; }',
        'green-black': 'body { background: black; color: white; } table { border-color: green; } th { background: darkgreen; }',
        'red-black': 'body { background: black; color: white; } table { border-color: red; } th { background: maroon; }',
        'white-blue': 'body { background: white; color: black; } table { border-color: blue; } th { background: lightblue; }',
        'soft-palette': 'body { background: #f0f8ff; color: #333; } table { border-color: #add8e6; } th { background: #e0ffff; }'  # Softer blues and lights
    }
    
    style = themes.get(selected_theme, themes['blue-black'])
    
    # HTML with alert table and theme selector
    html = f"""
    <style>{style}</style>
    <h1>VibeSIEM Dashboard</h1>
    <form method="POST">
        <label for="theme">Choose Color Scheme:</label>
        <select name="theme" id="theme">
            <option value="blue-black">Blue & Black</option>
            <option value="green-black">Green & Black</option>
            <option value="red-black">Red & Black</option>
            <option value="white-blue">White & Blue</option>
            <option value="soft-palette">Softer Palette</option>
        </select>
        <button type="submit">Apply</button>
    </form>
    <h2>Recent Alerts ({len(recent_alerts)})</h2>
    <table class="table table-striped">
        <thead><tr><th>Timestamp</th><th>Source IP</th><th>Event Type</th><th>Anomaly Score</th></tr></thead>
        <tbody>
            {"".join([f"<tr><td>{a['timestamp']}</td><td>{a['source_ip']}</td><td>{a['event_type']}</td><td>{a.get('anomaly_score', 'N/A')}</td></tr>" for a in recent_alerts])}
        </tbody>
    </table>
    <p>Total Anomalies Detected: {sum(1 for a in recent_alerts if a.get('anomaly_score', 0) < 0)}</p>
    """
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
