#!/bin/bash
mkdir -p ~/.kaggle
printf '%s' '{"username":"bolong0916","key":"51e83f1c34ab2cd072a7bba1f3184b22"}' > ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
export PATH=/usr/local/bin:$PATH
echo "kaggle.json created with size $(wc -c < ~/.kaggle/kaggle.json) bytes"
ls -la ~/.kaggle/
echo "Testing kaggle auth..."
kaggle datasets list -s creditcardfraud 2>&1 | head -3