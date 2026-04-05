#!/bin/bash
# 栀言书院 一键部署脚本（在服务器上运行）

echo "=== 栀言书院 部署脚本 ==="

# 安装 Docker
if ! command -v docker &> /dev/null; then
    echo "安装 Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
fi

# 安装 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "安装 Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# 克隆代码
if [ ! -d "/opt/zhiyan" ]; then
    echo "克隆代码..."
    git clone https://github.com/lfzds4399-cpu/miao-study.git /opt/zhiyan
else
    echo "更新代码..."
    cd /opt/zhiyan && git pull
fi

cd /opt/zhiyan

# 配置环境变量
if [ ! -f ".env" ]; then
    echo "配置 API Keys..."
    read -p "输入 ANTHROPIC_API_KEY: " ANTHROPIC_KEY
    read -p "输入 OPENAI_API_KEY: " OPENAI_KEY
    echo "ANTHROPIC_API_KEY=$ANTHROPIC_KEY" > .env
    echo "OPENAI_API_KEY=$OPENAI_KEY" >> .env
    echo "环境变量已保存"
fi

# 启动
echo "启动服务..."
docker-compose down 2>/dev/null
docker-compose up -d --build

echo ""
echo "=== 部署完成! ==="
echo "访问地址: http://$(curl -s ifconfig.me)"
echo ""
