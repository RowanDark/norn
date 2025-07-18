import smtplib
from email.mime.text import MIMEText

def execute_playbook(alert):
    if 'brute_force' in alert['event_type']:
        # Mock isolation: In real, integrate with firewall API
        print(f"Isolating IP: {alert['source_ip']} via playbook.")
        # Example: requests.post('firewall/api/block', data={'ip': alert['source_ip']})
    
    # Send email alert
    msg = MIMEText(f"Alert: {alert['event_type']} from {alert['source_ip']}")
    msg['Subject'] = 'VibeSIEM Alert'
    msg['From'] = 'siem@vibe.com'
    msg['To'] = 'admin@vibe.com'
    
    with smtplib.SMTP('localhost') as server:  # Configure real SMTP
        server.sendmail(msg['From'], msg['To'], msg.as_string())
    print("Playbook executed: Email sent.")

# Usage: In analyzer, after detecting alerts: for _, alert in alerts.iterrows(): execute_playbook(alert)
