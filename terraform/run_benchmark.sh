#!/bin/bash
set -e
cd ~
mkdir -p ml-benchmark
echo "=== STARTING BENCHMARK ==="
date
echo "=== DOWNLOADING DATASET ==="
kaggle datasets download -d mlg-ulb/creditcardfraud --unzip -p ./ml-benchmark/ 2>&1
echo "=== DATASET READY ==="
ls -lh ml-benchmark/
echo "=== RUNNING benchmark.py ==="
cd ml-benchmark
python3 ~/benchmark.py < /dev/null
echo "=== BENCHMARK DONE ==="
date
echo "=== RESULT FILE ==="
cat benchmark_result.json