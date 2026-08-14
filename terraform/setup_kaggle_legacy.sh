#!/bin/bash
mkdir -p ~/.kaggle
printf '%s' '{"username":"bolong0916","key":"51e83f1c34ab2cd072a7bba1f3184b22"}' > ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
echo "kaggle.json created"
ls -la ~/.kaggle/
echo "Testing kaggle auth..."
kaggle datasets list -s creditcardfraud 2>&1 | head -3