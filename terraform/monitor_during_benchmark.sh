#!/bin/bash
echo "=== Start monitoring during benchmark ==="
echo "Timestamp: $(date)"
echo "BEFORE BENCHMARK:"
top -bn1 | head -10
echo ""
echo "Running benchmark..."
cd /home/ubuntu/ml-benchmark
python3 -c "
import time, os
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
t0=time.time()
df = pd.read_csv('creditcard.csv')
print(f'Loaded {len(df):,} rows in {time.time()-t0:.2f}s')
X = df.drop(columns=['Class']); y = df['Class'].astype(int)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
model = lgb.train({'objective':'binary','metric':'auc','learning_rate':0.05,'num_leaves':31,'verbose':-1,'is_unbalance':True}, lgb.Dataset(X_train, label=y_train), num_boost_round=500, valid_sets=[lgb.Dataset(X_test, label=y_test)], callbacks=[lgb.early_stopping(50), lgb.log_evaluation(50)])
"
echo ""
echo "DURING/AFTER BENCHMARK:"
top -bn1 | head -10
echo ""
echo "FREE - RAM Usage:"
free -h
echo ""
echo "VMSTAT:"
vmstat 1 3