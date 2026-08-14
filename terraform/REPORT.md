# Báo cáo Lab 16 — Cloud AI Environment Setup (AWS)

**Sinh viên:** Lương Bảo Long (bolong0916)
**Ngày:** 14/08/2026
**Region:** us-east-1
**Account ID:** 072945505480

---

## 1. Kết quả Benchmark (CPU + LightGBM)

| Metric | Kết quả |
|---|---|
| Thời gian load data | 2.21s |
| Thời gian training | 3.41s |
| Best iteration | 1 (early stopping) |
| AUC-ROC | **0.936367** |
| Accuracy | 0.978775 |
| F1-Score | 0.124547 |
| Precision | 0.067030 |
| Recall | 0.877551 |
| Inference latency (1 row) | 0.44 ms |
| Inference throughput (1000 rows × 10) | 1,523,152 rows/sec |

## 2. Cấu hình Compute Node

| Thuộc tính | Giá trị |
|---|---|
| Instance type | `t3.small` (đổi từ `t3.medium` do Free Tier) |
| vCPU | 2 |
| RAM | 1.9 GB |
| Disk | 29 GB (gp3) |
| AMI | Ubuntu 22.04 LTS (Canonical) |
| Software | Python 3.10.12, lightgbm 4.7.0, scikit-learn 1.7.2, pandas 2.3.3, numpy 2.2.6 |

## 3. Top Network & Resources

- **CPU load average (during benchmark)**: 0.28, 0.12, 0.08 — rất nhẹ
- **RAM sử dụng**: 257 MB / 1910 MB (≈13.5%)
- **Disk sử dụng**: 2.9 GB / 29 GB (≈10%)
- **Network RX**: 287 MB (dataset download)
- **Network TX**: 1 MB

## 4. Nhận xét

- **Training time rất nhanh** (3.4s) vì:
  - Dataset nhỏ (284K rows × 30 features = ~150MB)
  - LightGBM tối ưu cao với early stopping (best iteration = 1)
  - CPU t3.small (2 vCPU) đủ xử lý gradient boosting ở quy mô này
- **AUC-ROC = 0.936** tốt và cân bằng giữa fraud/non-fraud classes với `is_unbalance=True`
- **Inference rất nhanh** (0.44 ms/row, ~1.5M rows/sec) → cho thấy LightGBM CPU có thể serve real-time fraud detection ngay cả với instance nhỏ
- **Recall cao (87.75%)** quan trọng cho fraud detection (không miss fraud) nhưng **Precision thấp (6.7%)** cho thấy nhiều false positives — đây là đặc tính của dataset imbalance (chỉ 0.17% fraud), cần tuning threshold (>0.5) hoặc thêm SMOTE/focal loss
- **Lưu ý**: instance `t3.medium` không eligible cho Free Tier trong account này → đã đổi sang `t3.small` để tránh chi phí

## 5. Issues gặp phải

1. **`t3.medium` không Free Tier eligible** → đổi sang `t3.small` qua biến `-var cpu_instance_type=t3.small`
2. **Kaggle CLI version cũ** trên EC2 cần `kaggle.json` legacy thay vì `access_token` mới → workaround bằng cách ghi file JSON thủ công
3. **CRLF/LF issue** khi copy script từ Windows sang Linux → convert LF

## 6. Deliverables

1. ✅ `terraform/main.tf`, `variables.tf`, `outputs.tf`, `user_data_cpu.sh` (đã chạy thành công)
2. ✅ `terraform/benchmark.py` (script training + inference LightGBM)
3. ✅ `terraform/benchmark_result_ec2.json` (kết quả đầy đủ)
4. ✅ Screenshots: AWS Billing, EC2 Monitoring
5. ✅ Resource monitoring data (top, free -h, ip -s link)
6. ✅ Báo cáo này

---

## 7. Cleanup Status

→ Cần chạy `terraform destroy` ngay để tránh phát sinh chi phí (NAT Gateway ~$0.045/giờ).
