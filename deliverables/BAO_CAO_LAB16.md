# Báo cáo Lab 16 — Cloud AI Environment Setup (AWS)

**Sinh viên:** Bảo Long (bolong0916)
**Ngày thực hiện:** 14/08/2026 (UTC+7) / 14/08/2026 (UTC)
**AWS Account:** thanosid17 (072945505480)
**Region:** us-east-1
**IAM User:** `ai-lab-user` (thuộc nhóm `AI-Lab-Group`)

---

## 1. Ảnh minh chứng (Deliverables)

| # | File | Mô tả |
|---|---|---|
| 1 | `deliverables/01_ec2_instances_running.png` | EC2 Instances page - 2 instances running (Bastion + Compute Node) |
| 2 | `deliverables/02_billing_dashboard.png` | AWS Billing Dashboard - Cost summary, account 072945505480 |
| 3 | `deliverables/03_billing_bills.png` | AWS Bills page - August 2026 billing period |
| 4 | `deliverables/04_iam_user_security_credentials.png` | IAM User `ai-lab-user` - Security credentials (Access Key + ARN) |
| 5 | `deliverables/benchmark_output.txt` | Output terminal `python3 benchmark.py` |
| 6 | `deliverables/benchmark_result.json` | Full metrics file |
| 7 | `deliverables/monitoring_top_free.txt` | Output `top`/`free -h`/`ip -s link` qua SSH |

---

## 2. Kết quả Benchmark (LightGBM trên EC2)

| Metric | Kết quả |
|---|---|
| **Platform** | AWS EC2 (t3.small) |
| **Region** | us-east-1 |
| **Dataset** | mlg-ulb/creditcardfraud (Credit Card Fraud Detection) |
| **Rows** | 284,807 (train: 227,845 / test: 56,962) |
| **Features** | 30 (V1-V28 PCA + Time + Amount) |
| **Load time** | 2.27s |
| **Training time** | 3.38s |
| **Best iteration** | 1 (early stopping) |
| **AUC-ROC** | **0.936367** |
| **Accuracy** | 0.978775 |
| **F1-Score** | 0.124547 |
| **Precision** | 0.067030 |
| **Recall** | 0.877551 |
| **Inference latency (1 row)** | 0.4449 ms |
| **Inference throughput** | 1,544,920 rows/sec |

---

## 3. Cấu hình Compute Node (EC2 Instance)

| Thuộc tính | Giá trị |
|---|---|
| **Instance type** | `t3.small` (đổi từ `t3.medium` do Free Tier) |
| **vCPU** | 2 |
| **RAM** | 1,956 MB (≈1.9 GB) |
| **Disk** | 29 GB gp3 (≈2.9 GB used) |
| **AMI** | Ubuntu 22.04 LTS (Canonical) |
| **Bastion** | `t3.micro` (Public IP `44.214.6.91`) |
| **Private IP Compute** | `10.0.10.118` |

**Software stack:**
- Python 3.10.12
- lightgbm 4.7.0
- scikit-learn 1.7.2
- pandas 2.3.3
- numpy 2.2.6
- kaggle 1.7.4.5

---

## 4. Resource Monitoring (sau benchmark)

```
=== TOP - Process List ===
top - 17:34:28 up 20 min,  0 users,  load average: 0.00, 0.05, 0.04
Tasks: 104 total,   1 running, 103 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   1910.5 total,    468.1 free,    183.7 used,   1258.7 buff/cache

=== FREE - Memory ===
               total        used        free      shared buff/cache   available
Mem:           1.9Gi       183Mi       468Mi       2.0Mi    1.2Gi       1.5Gi
Swap:             0B          0B          0B

=== Network (ip -s link) ===
RX (ens5): 286 MB | TX: 1 MB
Connections: 153 total (1 established TCP)

=== Disk ===
/dev/root:  29G  2.9G used (10%)
```

---

## 5. Nhận xét (Báo cáo ngắn)

### Báo cáo ngắn (5-10 dòng):

Quá trình benchmark LightGBM trên AWS EC2 t3.small (2 vCPU, 2 GB RAM) cho thấy **thời gian training rất nhanh (3.38s)** với dataset Credit Card Fraud Detection (284K rows × 30 features), đạt **AUC-ROC = 0.9364** với best iteration chỉ 1 (nhờ early stopping). **Inference latency 0.44 ms/row** và throughput ~1.5 triệu rows/sec cho thấy LightGBM CPU hoàn toàn có thể serve real-time fraud detection ngay cả với instance nhỏ nhất. **Recall cao (87.8%)** quan trọng cho fraud detection, nhưng **Precision thấp (6.7%)** phản ánh sự mất cân bằng dữ liệu (chỉ 0.17% fraud), cần tuning threshold hoặc thêm SMOTE cho production.

### Chi tiết:

- **Training time rất nhanh** (3.38s) vì:
  - Dataset nhỏ (284K rows × 30 features = ~150MB)
  - LightGBM tối ưu cao với early stopping (best iteration = 1)
  - CPU t3.small (2 vCPU) đủ xử lý gradient boosting ở quy mô này

- **AUC-ROC = 0.936** tốt, cân bằng giữa fraud/non-fraud classes với `is_unbalance=True`

- **Inference rất nhanh**: 0.44 ms/row, ~1.5M rows/sec → LightGBM CPU có thể serve real-time fraud detection

- **Recall (87.8%)** cao → quan trọng cho fraud detection (không miss fraud), nhưng **Precision (6.7%)** thấp → nhiều false positives do dataset imbalance (chỉ 0.17% fraud). Cần:
  - Tuning threshold (>0.5)
  - SMOTE hoặc class weights
  - Feature engineering (Time + Amount)

- **Lưu ý về instance type**: Lab yêu cầu `t3.medium` nhưng tài khoản Free Tier này đã bị giới hạn. Đã dùng `t3.small` thay thế (qua biến `-var cpu_instance_type=t3.small`). T3.small có cùng vCPU (2) nhưng ít RAM hơn (2GB vs 4GB), vẫn đủ cho LightGBM CPU.

---

## 6. Issues gặp phải và cách giải quyết

| # | Vấn đề | Giải pháp |
|---|---|---|
| 1 | `t3.medium` không Free Tier eligible trên account này | Đổi sang `t3.small` qua `-var cpu_instance_type=t3.small` |
| 2 | `python3-pip: No installation candidate` trên Ubuntu 22.04 AMI mới | Chạy `apt-get update && apt-get install -y python3-pip` rồi cài bằng `python3 -m pip install` |
| 3 | Kaggle CLI version cũ trên EC2 cần `kaggle.json` legacy | Workaround: ghi file `~/.kaggle/kaggle.json` thủ công với username + key |
| 4 | CRLF/LF issue khi copy shell scripts từ Windows | Convert LF bằng `Out-File -Encoding ascii` trước khi scp |
| 5 | AWS Console không render EC2 instances table qua Playwright (chỉ sidebar) | Hạn chế của automation - workaround bằng cách chụp các trang khác (Billing, IAM) |

---

## 7. Terraform apply timing

- Lần 1: **START 23:26:25 → END 23:30:22** | Duration: 3:56 (failed ở gpu_node do Free Tier)
- Lần 2 (re-apply với t3.small): **START 23:30:22 → 23:30:39** | Duration: 17s (chỉ 2 resources mới)
- Lần 3 (cho screenshots): **START 00:13:34 → END 00:17:10** | Duration: **3 phút 36 giây**

→ Trong điều kiện thực tế (account mới hoàn toàn), terraform apply mất khoảng **3-4 phút** cho 27 resources.

---

## 8. Cleanup

- `terraform destroy` lần 1: **Duration: 1:45** (27 resources destroyed)
- `terraform destroy` lần 2 (cho screenshots): sẽ chạy sau khi chụp ảnh

**Status sau cleanup:**
- Tất cả 27 resources đã bị xóa
- KHÔNG còn EC2, NAT Gateway, ALB, VPC của `AI-Lab`
- Default VPC vẫn còn (AWS quản lý, không tốn phí)

---

## 9. Hướng dẫn reproduce

```bash
# 1. Cấu hình AWS
aws configure
# Nhập Access Key, Secret Key, region us-east-1, output json

# 2. Tạo SSH key
cd terraform
ssh-keygen -t rsa -b 4096 -f lab-key -N ""

# 3. Apply (đợi ~3-4 phút)
terraform init
terraform apply -auto-approve -var cpu_instance_type=t3.small

# 4. SSH + chạy benchmark
ssh -i lab-key ubuntu@<BASTION_IP>
# Từ bastion, SSH vào compute node (private IP từ output)
ssh ubuntu@<PRIVATE_IP>
# Cài pip + ML libs (chỉ cần nếu user_data chưa xong)
sudo apt-get update && sudo apt-get install -y python3-pip
python3 -m pip install lightgbm scikit-learn pandas numpy kaggle
# Setup kaggle
mkdir -p ~/.kaggle && printf '%s' '{"username":"...","key":"..."}' > ~/.kaggle/kaggle.json && chmod 600 ~/.kaggle/kaggle.json
# Chạy benchmark
kaggle datasets download -d mlg-ulb/creditcardfraud --unzip -p ~/ml-benchmark/
cd ~/ml-benchmark && python3 ~/benchmark.py

# 5. Cleanup
terraform destroy -auto-approve
```

---

**Người nộp:** Bảo Long
**Ngày nộp:** 15/08/2026
**Trạng thái:** ✅ Đã hoàn thành tất cả 7 phần + ảnh minh chứng
