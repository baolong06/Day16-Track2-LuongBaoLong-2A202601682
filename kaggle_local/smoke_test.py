"""
Run LightGBM training locally using the creditcard.csv downloaded earlier.
This is a smoke test to ensure the notebook script works before uploading to Kaggle.
"""
import time
import json
import os
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score, accuracy_score, f1_score,
    precision_score, recall_score, confusion_matrix
)

CSV_PATH = os.path.join(os.path.dirname(__file__), 'creditcard.csv')
print('Loading:', CSV_PATH)

t0 = time.time()
df = pd.read_csv(CSV_PATH)
load_time = time.time() - t0
print(f'Loaded {len(df):,} rows in {load_time:.2f}s')

X = df.drop(columns=['Class'])
y = df['Class'].astype(int)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

params = {
    'objective': 'binary',
    'metric': 'auc',
    'learning_rate': 0.05,
    'num_leaves': 31,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': -1,
    'is_unbalance': True,
}

t0 = time.time()
train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)
model = lgb.train(
    params, train_data, num_boost_round=500,
    valid_sets=[train_data, test_data],
    valid_names=['train', 'test'],
    callbacks=[lgb.early_stopping(50), lgb.log_evaluation(50)],
)
train_time = time.time() - t0
best_iter = model.best_iteration

y_pred_proba = model.predict(X_test, num_iteration=best_iter)
y_pred = (y_pred_proba >= 0.5).astype(int)

auc = roc_auc_score(y_test, y_pred_proba)
acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

# Latency
t0 = time.time()
for _ in range(100):
    _ = model.predict(X_test.iloc[[0]], num_iteration=best_iter)
latency_1 = (time.time() - t0) * 10  # ms per 1 row

# Throughput
sample_1000 = X_test.iloc[:1000].copy()
t0 = time.time()
for _ in range(10):
    _ = model.predict(sample_1000, num_iteration=best_iter)
throughput = 1000 * 10 / (time.time() - t0)

results = {
    'platform': 'Local (smoke test)',
    'dataset': 'mlg-ulb/creditcardfraud',
    'rows_total': int(len(df)),
    'rows_train': int(len(X_train)),
    'rows_test': int(len(X_test)),
    'features': int(X.shape[1]),
    'load_time_sec': round(load_time, 4),
    'train_time_sec': round(train_time, 4),
    'best_iteration': int(best_iter),
    'auc_roc': round(float(auc), 6),
    'accuracy': round(float(acc), 6),
    'f1_score': round(float(f1), 6),
    'precision': round(float(prec), 6),
    'recall': round(float(rec), 6),
    'confusion_matrix': cm.tolist(),
    'inference_latency_ms_1row': round(latency_1, 4),
    'inference_throughput_rows_per_sec': round(throughput, 2),
}

print(json.dumps(results, indent=2))
with open(os.path.join(os.path.dirname(__file__), 'benchmark_result_local.json'), 'w') as f:
    json.dump(results, f, indent=2)
print('Done')
