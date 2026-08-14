#!/bin/bash
echo "=== Installing Python pip + LightGBM + kaggle ==="
sudo apt-get update -y 2>&1 | tail -3
sudo apt-get install -y python3-pip 2>&1 | tail -3
sudo apt-get install -y python3-dev build-essential 2>&1 | tail -3
python3 -m pip install --upgrade pip 2>&1 | tail -3
python3 -m pip install lightgbm scikit-learn pandas numpy kaggle 2>&1 | tail -5
echo "=== Verification ==="
python3 -c "import lightgbm; print('lightgbm:', lightgbm.__version__)"
python3 -c "import sklearn; print('sklearn:', sklearn.__version__)"
python3 -c "import pandas; print('pandas:', pandas.__version__)"
python3 -c "import numpy; print('numpy:', numpy.__version__)"
which kaggle
kaggle --version 2>&1 | head -2