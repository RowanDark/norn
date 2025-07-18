from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd

def normalize_logs(logs):
    logs['normalized_event'] = logs['event_type'].str.lower()
    logs['hour'] = logs['timestamp'].dt.hour  # Add time-based feature
    return logs

def train_and_detect(logs, labeled_data=None):
    # Feature engineering
    features = pd.get_dummies(logs[['source_ip', 'normalized_event', 'hour']])
    
    if labeled_data is not None:
        # Supervised refinement: Train Random Forest on labeled data
        X_train, X_test, y_train, y_test = train_test_split(features, labeled_data['label'], test_size=0.2)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        print(classification_report(y_test, predictions))  # Evaluate
        logs['prediction'] = model.predict(features)
        alerts = logs[logs['prediction'] == 'anomalous']
    else:
        # Fallback to unsupervised
        model = IsolationForest(contamination=0.1, random_state=42)
        model.fit(features)
        logs['anomaly_score'] = model.decision_function(features)
        alerts = logs[logs['anomaly_score'] < 0]
    
    # Basic rule-based on top
    rule_alerts = logs[logs['event_type'].str.contains('brute_force|denied', case=False)]
    combined_alerts = pd.concat([alerts, rule_alerts]).drop_duplicates()
    return combined_alerts

# Usage: Provide labeled_data as a DataFrame with 'label' column (e.g., 'normal' or 'anomalous')
# alerts = train_and_detect(normalized_logs, labeled_data=my_labeled_df)

