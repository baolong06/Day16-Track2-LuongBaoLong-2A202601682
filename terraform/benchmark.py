#!/usr/bin/env python3
"""
benchmark.py - AI Lab 16: Credit Card Fraud Detection with LightGBM
Designed for AWS EC2 CPU instance (t3.medium).
"""

import os
import sys
import json
import time
import subprocess

import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score, accuracy_score, f1_score,
    precision_score, recall_score, confusion_matrix,
)

CSV_PATH = os.path.expanduser('~/ml-benchmark/creditcard.csv')
RESULT_PATH = os.path.expanduser('~/ml-benchmark/benchmark_result.json')


def install_kaggle_if_missing():
    """Kaggle CLI đã được cài từ user_data, nhưng cần credentials."""
    kaggle_dir = os.path.expanduser('~/.kaggle')
    kaggle_json = os.path.join(kaggle_dir, 'kaggle.json')
    if os.path.exists(kaggle_json):
        print('[OK] Kaggle credentials found.')
        return
    print('[!] Kaggle credentials not found at', kaggle_json)
    print('Please paste your kaggle.json content below.')
    print('  (Get it from https://www.kaggle.com/settings/account -> Create New Token)')
    print()
    raw = input('Paste JSON here (single line): ').strip()
    os.makedirs(kaggle_dir, exist_ok=True)
    with open(kaggle_json, 'w') as f:
        f.write(raw)
    os.chmod(kaggle_json, 0o600)
    print('[OK] Saved kaggle.json')


def download_dataset():
    """Download creditcard.csv via Kaggle CLI (idempotent)."""
    if os.path.exists(CSV_PATH):
        size_mb = os.path.getsize(CSV_PATH) / 1024 / 1024
        print(f'[OK] Dataset already exists ({size_mb:.1f} MB)')
        return

    print('[*] Downloading Credit Card Fraud dataset from Kaggle...')
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    cmd = ['kaggle', 'datasets', 'download', '-d', 'mlg-ulb/creditcardfraud',
           '--unzip', '-p', os.path.dirname(CSV_PATH)]
    subprocess.run(cmd, check=True)


def main():
    print('=' * 60)
    print('AI Lab 16 - LightGBM Credit Card Fraud Detection Benchmark')
    print('=' * 60)
    print()

    # Step 0: ensure Kaggle creds + dataset
    install_kaggle_if_missing()
    download_dataset()

    # Step 1: load data
    print('\n[1] Loading dataset...')
    t0 = time.time()
    df = pd.read_csv(CSV_PATH)
    load_time = time.time() - t0
    print(f'    Loaded {len(df):,} rows, {df.shape[1]} columns in {load_time:.2f}s')
    print('    Class distribution:')
    print(df['Class'].value_counts().to_dict())

    # Step 2: split
    X = df.drop(columns=['Class'])
    y = df['Class'].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y,
    )
    print(f'\n[2] Train: {len(X_train):,} rows | Test: {len(X_test):,} rows')
    print(f'    Fraud ratio (train): {y_train.mean():.6f}')
    print(f'    Fraud ratio (test):  {y_test.mean():.6f}')

    # Step 3: train
    print('\n[3] Training LightGBM...')
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
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    t0 = time.time()
    model = lgb.train(
        params,
        train_data,
        num_boost_round=500,
        valid_sets=[train_data, test_data],
        valid_names=['train', 'test'],
        callbacks=[lgb.early_stopping(50), lgb.log_evaluation(50)],
    )
    train_time = time.time() - t0
    best_iter = model.best_iteration
    print(f'\n    Training time: {train_time:.2f}s | Best iteration: {best_iter}')

    # Step 4: evaluate
    print('\n[4] Evaluating...')
    y_pred_proba = model.predict(X_test, num_iteration=best_iter)
    y_pred = (y_pred_proba >= 0.5).astype(int)

    auc = roc_auc_score(y_test, y_pred_proba)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    print(f'    AUC-ROC:   {auc:.6f}')
    print(f'    Accuracy:  {acc:.6f}')
    print(f'    F1-Score:  {f1:.6f}')
    print(f'    Precision: {prec:.6f}')
    print(f'    Recall:    {rec:.6f}')
    print(f'    Confusion Matrix:')
    print(f'      {cm}')

    # Step 5: inference latency / throughput
    print('\n[5] Inference benchmark...')
    # Latency: predict 1 row, repeat 100 times, take avg
    single_row = X_test.iloc[[0]]
    t0 = time.time()
    for _ in range(100):
        _ = model.predict(single_row, num_iteration=best_iter)
    latency_1 = (time.time() - t0) * 10  # avg ms per row

    # Throughput: 1000 rows, repeat 10x
    sample_1000 = X_test.iloc[:1000].copy()
    t0 = time.time()
    for _ in range(10):
        _ = model.predict(sample_1000, num_iteration=best_iter)
    elapsed = time.time() - t0
    throughput = 1000 * 10 / elapsed

    print(f'    Latency (1 row):    {latency_1:.4f} ms')
    print(f'    Throughput (1000x10): {throughput:.2f} rows/sec')

    # Step 6: save
    print('\n[6] Saving results...')
    results = {
        'platform': 'AWS EC2 t3.medium (CPU)',
        'region': os.environ.get('AWS_REGION', 'us-east-1'),
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

    with open(RESULT_PATH, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'    Saved to: {RESULT_PATH}')
    print()
    print(json.dumps(results, indent=2))
    print('\n[OK] Done.')


if __name__ == '__main__':
    main()
