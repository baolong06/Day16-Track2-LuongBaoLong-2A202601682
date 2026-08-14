#!/bin/bash
echo "=== Setting up Kaggle auth ==="
mkdir -p ~/.kaggle
cp ~/kaggle.json ~/.kaggle/kaggle.json 2>/dev/null || true
[ -s ~/.kaggle/kaggle.json ] || printf '%s' '{"username":"bolong0916","key":"51e83f1c34ab2cd072a7bba1f3184b22"}' > ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
echo "kaggle.json size: $(wc -c < ~/.kaggle/kaggle.json) bytes"

export PATH=/home/ubuntu/.local/bin:/usr/local/bin:$PATH
echo "=== PATH: $PATH ==="
echo "=== kaggle version ==="
kaggle --version

echo "=== Downloading dataset ==="
mkdir -p ~/ml-benchmark
kaggle datasets download -d mlg-ulb/creditcardfraud --unzip -p ~/ml-benchmark/ 2>&1 | tail -5

echo "=== ls dataset ==="
ls -lh ~/ml-benchmark/

echo "=== Running benchmark.py ==="
date
python3 ~/benchmark.py
date