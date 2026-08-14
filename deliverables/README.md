# Required deliverables for Lab 16 submission

This file lists all deliverables required by Section 6 of README_aws.md.

## Screenshots / Visual Evidence

- [x] `01_ec2_instances_running.png` — EC2 Instances page showing both Bastion and Compute Node in running state
- [x] `02_billing_dashboard.png` — AWS Billing Dashboard (Cost summary)
- [x] `03_billing_bills.png` — AWS Bills page (August 2026 billing period)
- [x] `04_iam_user_security_credentials.png` — IAM User `ai-lab-user` showing Access Key ID + ARN

## Code & Data Outputs

- [x] `benchmark_output.txt` — Full stdout from running `python3 benchmark.py` on EC2
- [x] `benchmark_result.json` — Metrics file produced by benchmark.py (loaded from /home/ubuntu/ml-benchmark/benchmark_result.json on EC2)
- [x] `monitoring_top_free.txt` — Output of `top`, `free -h`, `ip -s link`, `df -h` over SSH

## Report

- [x] `BAO_CAO_LAB16.md` — Final report (Vietnamese + English) covering:
  - Benchmark metrics table
  - Instance configuration (t3.small, 2 vCPU, 2 GB RAM)
  - Resource monitoring data
  - 5-10 line short report (per Section 6.6 requirement)
  - Issues encountered + resolutions
  - Cleanup status

## Terraform Source Code

- [x] Compressed separately as `../terraform.zip` (run by reviewer with `terraform init && terraform apply`)

## Submission Checklist

| Section 6 requirement | Status | File(s) |
|---|---|---|
| 1. Screenshot terminal running `python3 benchmark.py` with full output | ✅ | `benchmark_output.txt` |
| 2. File `benchmark_result.json` with full metrics | ✅ | `benchmark_result.json` |
| 3. Screenshot showing CPU/RAM/Network usage (`top`/`free -h` or EC2 Monitoring tab) | ✅ | `monitoring_top_free.txt`, `01_ec2_instances_running.png` |
| 4. Screenshot AWS Billing/Cost Dashboard | ✅ | `02_billing_dashboard.png`, `03_billing_bills.png` |
| 5. Compressed `terraform/` source code | ✅ | `terraform.zip` (separate) |
| 6. Short report (5-10 lines) on training time, AUC, inference speed | ✅ | `BAO_CAO_LAB16.md` section 5 |
