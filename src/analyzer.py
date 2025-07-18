from sklearn.ensemble import IsolationForest
import pandas as pd

def normalize_logs(logs):
    # Standardize to JSON-like structure
    logs['normalized_event'] = logs['event_type'].str.lower()
    return logs

def detect_anomalies(logs):
    # Basic rule-based detection
    alerts = logs[logs['event_type'].str.contains('brute_force|denied', case=False)]
    
    # AI enhancement: Use Isolation Forest for anomaly detection
    model = IsolationForest(contamination=0.1, random_state=42)
    features = pd.get_dummies(logs[['source_ip', 'normalized_event']])  # Simple feature engineering
    model.fit(features)
    logs['anomaly_score'] = model.decision_function(features)
    ai_alerts = logs[logs['anomaly_score'] < 0]  # Threshold for anomalies
    
    combined_alerts = pd.concat([alerts, ai_alerts]).drop_duplicates()
    return combined_alerts

# Usage: normalized = normalize_logs(logs)
# alerts = detect_anomalies(normalized)
