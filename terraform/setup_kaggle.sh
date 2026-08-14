#!/bin/bash
# setup_kaggle.sh - Set up Kaggle credentials on compute node
mkdir -p ~/.kaggle
echo "KGAT_ac453218c6620a8a76f579a8632d14df" > ~/.kaggle/access_token
chmod 600 ~/.kaggle/access_token
echo "Kaggle access_token installed at ~/.kaggle/access_token"
ls -la ~/.kaggle/
cat ~/.kaggle/access_token