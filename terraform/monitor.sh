#!/bin/bash
echo "=== TOP - CPU Usage (snapshot) ==="
top -bn1 | head -20
echo ""
echo "=== FREE - RAM Usage ==="
free -h
echo ""
echo "=== IP - Network Usage ==="
ip -s link
echo ""
echo "=== DF - Disk Usage ==="
df -h
echo ""
echo "=== System info ==="
uname -a
echo "Uptime: $(uptime)"
echo "vCPU info:"
grep -c processor /proc/cpuinfo
echo "Memory total:"
grep MemTotal /proc/meminfo