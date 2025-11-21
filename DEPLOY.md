# Deploy lên Naver Cloud VPC

## Bước 1: Tạo VPC Server trên Naver Cloud

1. Tạo Server (Ubuntu 20.04 hoặc 22.04)
2. Cấu hình Security Group: Mở port **3000** và **22** (SSH)
3. Lấy Public IP của server

## Bước 2: Upload code lên server

```bash
# Nén project (không bao gồm node_modules và model)
tar -czf classifier-api.tar.gz \
  --exclude=node_modules \
  --exclude=bert_classifier \
  --exclude=__pycache__ \
  *.js *.py *.csv *.json *.txt

# Upload lên server
scp classifier-api.tar.gz ubuntu@<SERVER_IP>:/home/ubuntu/

# SSH vào server
ssh ubuntu@<SERVER_IP>

# Giải nén
mkdir -p /home/ubuntu/classifier-api
tar -xzf classifier-api.tar.gz -C /home/ubuntu/classifier-api
```

## Bước 3: Upload model riêng (file lớn)

```bash
# Nén thư mục model
tar -czf bert_classifier.tar.gz bert_classifier/

# Upload lên server
scp bert_classifier.tar.gz ubuntu@<SERVER_IP>:/home/ubuntu/

# SSH vào server và giải nén
ssh ubuntu@<SERVER_IP>
tar -xzf bert_classifier.tar.gz -C /home/ubuntu/classifier-api/
```

## Bước 4: Chạy deploy script

```bash
ssh ubuntu@<SERVER_IP>
cd /home/ubuntu/classifier-api
chmod +x deploy.sh
./deploy.sh
```

## Bước 5: Kiểm tra

```bash
# Xem trạng thái
pm2 status

# Xem logs
pm2 logs classifier-api

# Test API
curl -X POST http://localhost:3000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "When was Hue Imperial City built?"}'
```

## Các lệnh quản lý

```bash
pm2 restart classifier-api  # Restart
pm2 stop classifier-api     # Stop
pm2 delete classifier-api   # Xóa
pm2 logs classifier-api     # Xem logs
pm2 monit                   # Monitor real-time
```

## Cấu hình Security Group trên Naver Cloud

- **Inbound Rules:**
  - Port 22 (SSH): 0.0.0.0/0
  - Port 3000 (API): 0.0.0.0/0 hoặc chỉ IP cần thiết

## Note

- Server cần ít nhất **2GB RAM** để chạy model BERT
- Model sẽ load khoảng 2-3 giây lần đầu
- PM2 sẽ tự động restart nếu app crash
