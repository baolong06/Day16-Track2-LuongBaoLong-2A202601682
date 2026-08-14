#!/bin/bash
echo "=== System info ==="
uname -a
echo "=== Python info ==="
which python3
python3 --version
echo "=== Pip info ==="
which pip3
pip3 --version
echo "=== Try import lightgbm ==="
python3 -c "import lightgbm; print('lightgbm:', lightgbm.__version__)"
echo "=== Try import sklearn ==="
python3 -c "import sklearn; print('sklearn:', sklearn.__version__)"
echo "=== Try import pandas ==="
python3 -c "import pandas; print('pandas:', pandas.__version__)"
echo "=== Try import numpy ==="
python3 -c "import numpy; print('numpy:', numpy.__version__)"
echo "=== DONE ==="