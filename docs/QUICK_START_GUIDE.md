# 展会信息查询助手 - 快速使用指南

## ✅ 已完成的工作

我已经为你创建了完整的REST API服务，所有功能都已测试通过！

### 📁 创建的文件

```
src/
├── api/
│   └── main.py                 # FastAPI服务主文件
├── tools/
│   ├── exhibition_core.py      # 展会查询核心逻辑
│   ├── image_recognition_core.py # 图片识别核心逻辑
│   └── excel_generation_core.py  # Excel生成核心逻辑
scripts/
├── start_api.sh                # API启动脚本
└── test_api.py                 # API测试脚本
docs/
└── API_DEPLOYMENT_GUIDE.md     # 详细部署文档
```

### ✅ 测试结果

```
✅ 展会信息查询测试通过
✅ 展商名录搜索测试通过
✅ Excel生成测试通过

所有测试通过！API服务准备就绪
```

---

## 🚀 下一步操作指南

### 方案一：本地测试API服务

**1. 启动API服务**

```bash
cd src/api
python main.py
```

服务将在 `http://localhost:8000` 启动

**2. 访问API文档**

打开浏览器访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**3. 测试API接口**

使用curl或Postman测试：

```bash
# 测试展会查询
curl -X POST http://localhost:8000/api/search_exhibition \
  -H "Content-Type: application/json" \
  -d '{"exhibition_name": "广交会"}'

# 测试展商搜索
curl -X POST http://localhost:8000/api/search_exhibitors \
  -H "Content-Type: application/json" \
  -d '{"exhibition_name": "广交会"}'
```

---

### 方案二：部署到云服务器（用于企业微信对接）

**步骤1：准备服务器**

需要一台公网可访问的服务器，推荐：
- 阿里云ECS
- 腾讯云CVM
- 华为云ECS

**步骤2：安装环境**

```bash
# 安装Python 3.9+
sudo apt update
sudo apt install python3 python3-pip

# 安装依赖
pip3 install fastapi uvicorn pydantic
```

**步骤3：上传代码**

将整个项目上传到服务器

**步骤4：启动服务**

```bash
cd /path/to/project/src/api
nohup python3 main.py > api.log 2>&1 &
```

**步骤5：配置域名和HTTPS**

企业微信要求HTTPS，需要：
1. 购买域名（可选，也可以用IP）
2. 申请SSL证书（推荐Let's Encrypt免费证书）
3. 配置Nginx反向代理

**示例Nginx配置：**

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

### 方案三：在企业微信AI+平台配置

**前提条件：**
- API服务已部署并可通过HTTPS访问
- 例如：`https://your-domain.com/api/chat`

**配置步骤：**

1. **登录企业微信管理后台**
   - 访问：https://work.weixin.qq.com/

2. **创建智能机器人**
   - 进入"应用管理" → "机器人"
   - 点击"创建机器人"
   - 填写基本信息：
     - 名称：展会查询助手
     - 简介：帮助企业快速查询展会信息

3. **配置系统对接**
   - 选择"系统对接"
   - 填写API地址：`https://your-domain.com/api/chat`
   - 设置超时时间：30秒
   - 测试连接

4. **配置使用场景**
   - 勾选"单聊/群聊直接使用"
   - 设置欢迎语
   - 配置触发关键词

5. **发布机器人**
   - 选择可见范围
   - 点击发布

---

## 📋 API接口清单

### 主要接口

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/chat` | POST | 智能对话（企业微信对接主接口） |
| `/api/search_exhibition` | POST | 查询展会信息 |
| `/api/search_exhibitors` | POST | 搜索参展商名录 |
| `/api/search_by_keywords` | POST | 关键词搜索展会 |
| `/api/recognize_image` | POST | 识别图片展商 |
| `/api/batch_recognize` | POST | 批量识别图片 |
| `/api/generate_excel` | POST | 生成Excel表格 |
| `/api/json_to_excel` | POST | JSON转Excel |

### 接口示例

**查询展会信息：**

```bash
POST /api/search_exhibition
Content-Type: application/json

{
  "exhibition_name": "广交会"
}
```

**生成Excel表格：**

```bash
POST /api/generate_excel
Content-Type: application/json

{
  "exhibitors_data": [
    {"公司名称": "华为", "展位号": "A01"},
    {"公司名称": "比亚迪", "展位号": "A02"}
  ],
  "file_name": "exhibitor_list"
}
```

---

## 🔧 常见问题

### Q1: 如何验证API服务是否正常？

访问：`http://your-domain:8000/health`
返回：`{"status": "healthy"}` 表示正常

### Q2: 企业微信对接需要什么条件？

- ✅ 公网可访问的服务器
- ✅ HTTPS配置完成
- ✅ API服务正常运行

### Q3: 如何查看API日志？

```bash
# 查看实时日志
tail -f api.log

# 查看最近100行
tail -n 100 api.log
```

### Q4: 如何停止API服务？

```bash
# 查找进程
ps aux | grep python

# 停止进程
kill <PID>
```

---

## 📞 技术支持

如遇到问题，请检查：
1. API服务是否正常运行
2. 端口是否被占用（默认8000）
3. 防火墙是否开放端口
4. HTTPS证书是否有效

---

## 🎉 完成状态

- ✅ API服务已创建
- ✅ 所有接口已实现
- ✅ 功能测试通过
- ✅ 部署文档已提供
- ✅ 企业微信对接指南已提供

**你现在可以：**
1. 本地测试API服务
2. 部署到云服务器
3. 在企业微信AI+平台配置对接

**需要帮助？**
- 查看 `docs/API_DEPLOYMENT_GUIDE.md` 获取详细部署说明
- 查看 `http://localhost:8000/docs` 查看API文档

祝使用顺利！🚀
