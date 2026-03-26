# API服务云服务器部署完整指南

## 🎯 部署方案对比

| 方案 | 难度 | 费用 | HTTPS | 适用场景 |
|------|------|------|-------|----------|
| Railway/Render | ⭐ | 免费/低价 | ✅ 自动 | 测试、小型应用 |
| 阿里云/腾讯云 | ⭐⭐⭐ | 按量付费 | 需配置 | 正式使用 |
| Docker部署 | ⭐⭐ | 服务器费用 | 需配置 | 团队协作 |

---

## 方案一：Railway.app 部署（最简单）

### 前提条件
- GitHub 账号
- 项目代码已上传到 GitHub

### 步骤详解

#### 1. 修改代码以支持云部署

**创建 `Procfile` 文件**

在 `src/api/` 目录下创建 `Procfile` 文件（无扩展名）：

```
web: python main.py
```

**修改 `src/api/main.py`**

找到文件末尾的启动代码，修改为：

```python
if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
```

#### 2. 部署到 Railway

1. 访问 https://railway.app/
2. 点击 "Start a New Project"
3. 选择 "Deploy from GitHub repo"
4. 授权 Railway 访问你的 GitHub
5. 选择你的项目仓库
6. 配置项目：
   - **Root Directory**: `src/api`
   - **Build Command**: 自动检测
   - **Start Command**: 自动从 Procfile 读取
7. 点击 "Deploy"

#### 3. 获取API地址

部署成功后，Railway 会提供一个地址：
```
https://your-project-name.railway.app
```

测试API：
```bash
curl https://your-project-name.railway.app/health
```

#### 4. 自定义域名（可选）

在 Railway 项目设置中：
1. 点击 "Settings" → "Domains"
2. 添加自定义域名
3. 按照提示配置 DNS

---

## 方案二：阿里云ECS部署（推荐正式使用）

### 第一步：购买服务器

#### 1. 选择配置

推荐配置：
- **CPU**: 2核
- **内存**: 4GB
- **带宽**: 3Mbps
- **系统**: Ubuntu 22.04 LTS
- **地域**: 根据用户位置选择

费用参考：约 ¥100-200/月

#### 2. 购买流程

1. 访问 https://www.aliyun.com/product/ecs
2. 选择"按量付费"或"包年包月"
3. 选择地域（推荐：华东、华北）
4. 选择实例规格（推荐：2核4G）
5. 选择镜像：Ubuntu 22.04
6. 设置密码（记住这个密码）
7. 确认订单并支付

### 第二步：连接服务器

#### Windows用户

1. 下载 PuTTY 或使用 Windows Terminal
2. SSH连接：
```bash
ssh root@你的服务器IP
# 输入密码
```

#### Mac/Linux用户

```bash
ssh root@你的服务器IP
# 输入密码
```

### 第三步：安装环境

连接到服务器后，依次执行：

```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装Python 3和pip
sudo apt install python3 python3-pip python3-venv -y

# 3. 安装Nginx（用于反向代理）
sudo apt install nginx -y

# 4. 安装Git
sudo apt install git -y

# 5. 检查Python版本
python3 --version
# 应该显示 Python 3.10.x 或更高
```

### 第四步：上传代码

#### 方式A：使用Git（推荐）

```bash
# 创建项目目录
mkdir -p /opt/exhibition-api
cd /opt/exhibition-api

# 克隆代码（替换为你的仓库地址）
git clone https://github.com/你的用户名/你的仓库.git .

# 或者直接上传文件（见方式B）
```

#### 方式B：使用SCP上传

在本地电脑上：
```bash
# 打包项目
cd /path/to/your/project
tar -czf exhibition-api.tar.gz src/ config/ requirements.txt

# 上传到服务器
scp exhibition-api.tar.gz root@你的服务器IP:/opt/

# SSH到服务器解压
ssh root@你的服务器IP
cd /opt
tar -xzf exhibition-api.tar.gz
```

### 第五步：配置Python环境

```bash
# 进入项目目录
cd /opt/exhibition-api

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装Gunicorn（生产服务器）
pip install gunicorn
```

### 第六步：测试运行

```bash
# 进入API目录
cd src/api

# 测试运行
python main.py

# 看到以下输出表示成功：
# INFO:     Uvicorn running on http://0.0.0.0:8000

# 按 Ctrl+C 停止测试
```

### 第七步：配置Systemd服务（让API在后台持续运行）

创建服务文件：
```bash
sudo nano /etc/systemd/system/exhibition-api.service
```

粘贴以下内容：
```ini
[Unit]
Description=Exhibition API Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/exhibition-api/src/api
Environment="PATH=/opt/exhibition-api/venv/bin"
ExecStart=/opt/exhibition-api/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

保存并退出（Ctrl+O 保存，Ctrl+X 退出）

启动服务：
```bash
# 重新加载systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start exhibition-api

# 设置开机自启
sudo systemctl enable exhibition-api

# 查看状态
sudo systemctl status exhibition-api

# 查看日志
sudo journalctl -u exhibition-api -f
```

### 第八步：配置Nginx反向代理

```bash
# 编辑Nginx配置
sudo nano /etc/nginx/sites-available/exhibition-api
```

粘贴以下内容：
```nginx
server {
    listen 80;
    server_name 你的服务器IP或域名;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

启用配置：
```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/exhibition-api /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

### 第九步：配置HTTPS（企业微信要求）

#### 使用 Let's Encrypt 免费证书

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 申请证书（需要域名）
sudo certbot --nginx -d 你的域名.com

# 按照提示输入邮箱，同意条款

# 自动续期测试
sudo certbot renew --dry-run
```

**如果没有域名，只有IP：**

企业微信必须使用HTTPS，你需要：
1. 购买域名（阿里云/腾讯云，约 ¥10-50/年）
2. 配置域名解析到服务器IP
3. 使用上面的Certbot申请证书

### 第十步：配置防火墙

```bash
# 开放HTTP和HTTPS端口
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22  # SSH

# 启用防火墙
sudo ufw enable

# 查看状态
sudo ufw status
```

### 第十一步：最终测试

```bash
# 测试HTTP
curl http://你的服务器IP/health

# 测试HTTPS（配置证书后）
curl https://你的域名.com/health

# 应该返回
{"status": "healthy"}
```

---

## 方案三：Docker部署（适合团队）

### 1. 创建Dockerfile

在项目根目录创建 `Dockerfile`：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY src/ ./src/
COPY config/ ./config/

WORKDIR /app/src/api

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "main.py"]
```

### 2. 构建镜像

```bash
docker build -t exhibition-api .
```

### 3. 运行容器

```bash
docker run -d -p 8000:8000 --name exhibition-api exhibition-api
```

### 4. 使用Docker Compose（可选）

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    restart: always
    environment:
      - PYTHONUNBUFFERED=1
```

运行：
```bash
docker-compose up -d
```

---

## 🔧 常见问题解决

### Q1: API无法访问？

```bash
# 检查服务是否运行
sudo systemctl status exhibition-api

# 检查端口是否监听
sudo netstat -tlnp | grep 8000

# 查看日志
sudo journalctl -u exhibition-api -n 50
```

### Q2: Nginx报错502 Bad Gateway？

```bash
# 检查API服务是否运行
sudo systemctl status exhibition-api

# 检查Nginx错误日志
sudo tail -f /var/log/nginx/error.log
```

### Q3: HTTPS证书申请失败？

- 确保域名已正确解析到服务器IP
- 确保80端口可访问
- 检查防火墙设置

### Q4: 内存不足？

```bash
# 查看内存使用
free -h

# 创建交换空间（临时增加内存）
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Q5: 如何查看API日志？

```bash
# 实时查看日志
sudo journalctl -u exhibition-api -f

# 查看最近100行
sudo journalctl -u exhibition-api -n 100
```

### Q6: 如何更新代码？

```bash
# 停止服务
sudo systemctl stop exhibition-api

# 更新代码
cd /opt/exhibition-api
git pull

# 重启服务
sudo systemctl start exhibition-api
```

---

## 📊 性能优化建议

### 1. 使用Gunicorn（多进程）

修改启动方式：
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 2. 启用Gzip压缩

在Nginx配置中添加：
```nginx
gzip on;
gzip_types text/plain application/json;
```

### 3. 配置缓存

对于不常变化的响应，可以配置Nginx缓存。

---

## 🔐 安全加固

### 1. 禁用root密码登录

```bash
# 创建新用户
sudo adduser deploy
sudo usermod -aG sudo deploy

# 配置SSH密钥登录
# 然后禁用密码登录
sudo nano /etc/ssh/sshd_config
# 设置：PasswordAuthentication no
```

### 2. 配置API认证

在 `main.py` 中添加API Key认证：

```python
from fastapi import Header, HTTPException

API_KEY = "your-secret-api-key"

async def verify_api_key(api_key: str = Header(None)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
```

---

## 💰 费用估算

| 项目 | 费用 | 备注 |
|------|------|------|
| 云服务器 | ¥100-200/月 | 2核4G配置 |
| 域名 | ¥10-50/年 | 可选 |
| SSL证书 | 免费 | Let's Encrypt |
| 带宽 | 包含在服务器中 | 3-5Mbps |

**总计：约 ¥100-200/月**

---

## 📞 部署检查清单

- [ ] 服务器已购买并可以SSH连接
- [ ] Python环境已安装
- [ ] 代码已上传到服务器
- [ ] 依赖已安装
- [ ] API服务可以本地运行
- [ ] Systemd服务已配置
- [ ] Nginx反向代理已配置
- [ ] 防火墙已配置
- [ ] HTTPS证书已配置（企业微信必须）
- [ ] API可以通过HTTP/HTTPS访问
- [ ] 日志可以正常查看

---

## 🎯 推荐方案

**个人测试/小型应用：** 使用 Railway.app
- 免费
- 自动HTTPS
- 部署简单

**正式使用/企业应用：** 使用阿里云ECS
- 稳定可靠
- 完全控制
- 支持自定义域名

---

## 📝 部署后验证

```bash
# 1. 测试健康检查
curl https://你的域名.com/health

# 2. 测试展会查询
curl -X POST https://你的域名.com/api/search_exhibition \
  -H "Content-Type: application/json" \
  -d '{"exhibition_name": "广交会"}'

# 3. 查看API文档
打开浏览器：https://你的域名.com/docs
```

---

祝部署顺利！🚀
