#!/bin/bash
# Deploy script cho Naver Cloud VPC

echo "========================================="
echo "Deploying Classifier API to Naver Cloud"
echo "========================================="

# 1. Update system
echo "[1/6] Updating system..."
sudo apt update && sudo apt upgrade -y

# 2. Install Node.js 18.x
echo "[2/6] Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 3. Install Python 3.10 và pip
echo "[3/6] Installing Python..."
sudo apt install -y python3 python3-pip python3-venv

# 4. Install PM2 globally
echo "[4/6] Installing PM2..."
sudo npm install -g pm2

# 5. Setup project directory
echo "[5/6] Setting up project..."
cd /home/ubuntu/classifier-api || exit

# Install Node dependencies
npm install

# Install Python dependencies
pip3 install -r requirements.txt

# 6. Start server with PM2
echo "[6/6] Starting server with PM2..."
pm2 delete classifier-api 2>/dev/null || true
pm2 start ecosystem.config.js
pm2 save
pm2 startup

echo "========================================="
echo "Deployment completed!"
echo "API running on port 3000"
echo "Check status: pm2 status"
echo "View logs: pm2 logs classifier-api"
echo "========================================="
