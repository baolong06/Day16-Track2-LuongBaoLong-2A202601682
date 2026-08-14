#!/bin/bash
echo "=== TOP - Process List (snapshot) ==="
top -bn1 | head -25
echo ""
echo "=== FREE - Memory ==="
free -h
echo ""
echo "=== IP -s link (Network) ==="
ip -s link
echo ""
echo "=== UPTIME ==="
uptime
echo ""
echo "=== CPU/MEM INFO ==="
echo "vCPUs: $(grep -c processor /proc/cpuinfo)"
grep MemTotal /proc/meminfo
echo ""
echo "=== DF - Disk ==="
df -h
echo ""
echo "=== Network connections ==="
ss -s
echo ""
echo "=== LightGBM check ==="
python3 -c "import lightgbm; print('LightGBM:', lightgbm.__version__)"