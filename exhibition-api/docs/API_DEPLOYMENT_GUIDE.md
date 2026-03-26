# 展会信息查询助手 - API服务部署文档

## 📋 概述

本API服务为展会信息查询助手提供RESTful接口，用于企业微信智能机器人AI+平台对接。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install fastapi uvicorn pydantic
```

### 2. 启动服务

```bash
cd src/api
python main.py
```

服务将在 `http://localhost:8000` 启动

### 3. 访问API文档

启动后访问以下地址查看自动生成的API文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📡 API接口说明

### 基础接口

#### GET /
API根路径，返回服务信息和可用端点列表

#### GET /health
健康检查接口

---

### 对话接口（企业微信AI+主要对接）

#### POST /api/chat

**用途**：智能对话接口，自动识别用户意图并执行相应操作

**请求示例**：
```json
{
  "query": "查询广交会信息",
  "user_id": "user123",
  "context": {}
}
```

**响应示例**：
```json
{
  "success": true,
  "message": "展会信息查询成功",
  "data": {
    "result": "## 广交会 展会信息\n..."
  }
}
```

---

### 展会信息查询

#### POST /api/search_exhibition

**用途**：查询展会的官方网站、时间地点、主办方等基本信息

**请求示例**：
```json
{
  "exhibition_name": "广交会",
  "user_id": "user123"
}
```

**响应示例**：
```json
{
  "success": true,
  "message": "已查询到 广交会 的相关信息",
  "data": {
    "result": "## 广交会 展会信息\n..."
  }
}
```

---

### 展商名录搜索

#### POST /api/search_exhibitors

**用途**：搜索展会的参展商名录、企业名单

**请求示例**：
```json
{
  "exhibition_name": "广交会参展商",
  "user_id": "user123"
}
```

**响应示例**：
```json
{
  "success": true,
  "message": "已找到 广交会参展商 的参展商信息",
  "data": {
    "result": "## 广交会参展商 参展商信息\n..."
  }
}
```

---

### 关键词搜索展会

#### POST /api/search_by_keywords

**用途**：根据关键词搜索相关展会，支持地区和时间筛选

**请求示例**：
```json
{
  "keywords": "电子展",
  "location": "深圳",
  "date_range": "2025年3月",
  "user_id": "user123"
}
```

---

### 图片识别

#### POST /api/recognize_image

**用途**：识别展会现场图片中的展商信息

**请求示例**：
```json
{
  "image_url": "https://example.com/exhibition.jpg",
  "user_id": "user123"
}
```

**响应示例**：
```json
{
  "success": true,
  "message": "图片识别成功",
  "data": {
    "result": "## 图片识别结果\n识别到 3 个展商信息..."
  }
}
```

---

### 批量图片识别

#### POST /api/batch_recognize

**用途**：批量识别多张展会图片，自动整合去重

**请求示例**：
```json
{
  "image_urls": [
    "https://example.com/img1.jpg",
    "https://example.com/img2.jpg"
  ],
  "user_id": "user123"
}
```

---

### Excel生成

#### POST /api/generate_excel

**用途**：将展商信息生成Excel表格，返回下载链接

**请求示例**：
```json
{
  "exhibitors_data": [
    {"公司名称": "华为技术有限公司", "展位号": "A01"},
    {"公司名称": "比亚迪股份有限公司", "展位号": "A02"}
  ],
  "file_name": "exhibitor_list",
  "user_id": "user123"
}
```

**响应示例**：
```json
{
  "success": true,
  "message": "Excel表格已生成",
  "data": {
    "result": "Excel文件已生成成功！\n下载链接：https://..."
  }
}
```

---

### JSON转Excel

#### POST /api/json_to_excel

**用途**：将JSON数据转换为Excel表格

**请求示例**：
```json
{
  "json_data": "[{\"姓名\":\"张三\",\"年龄\":25},{\"姓名\":\"李四\",\"年龄\":30}]",
  "file_name": "data_export",
  "user_id": "user123"
}
```

---

## 🔧 企业微信AI+平台配置指南

### 步骤1：部署API服务

将API服务部署到公网可访问的服务器，确保：
- 服务可通过公网IP或域名访问
- 端口8000（或其他端口）已开放
- HTTPS配置完成（企业微信要求）

### 步骤2：在企业微信AI+平台创建机器人

1. 登录企业微信管理后台
2. 进入"应用管理" → "机器人"
3. 点击"创建机器人"
4. 填写机器人基本信息：
   - 名称：展会查询助手
   - 头像：上传自定义头像
   - 简介：帮助企业快速查询展会信息

### 步骤3：配置系统对接

在机器人配置页面：
1. 选择"系统对接"
2. 填写API地址：
   - 主接口：`https://your-domain.com/api/chat`
   - 或配置各个独立接口
3. 设置请求头（如需认证）
4. 配置超时时间（建议30秒）

### 步骤4：配置使用场景

1. 选择"单聊/群聊直接使用"
2. 配置欢迎语：
   ```
   您好！我是展会查询助手，可以帮您：
   1. 查询展会信息
   2. 搜索参展商名录
   3. 识别展会图片
   4. 生成Excel表格
   
   请问您需要什么帮助？
   ```
3. 设置触发关键词

### 步骤5：测试机器人

1. 在企业微信中找到机器人
2. 发送测试消息："查询广交会信息"
3. 确认机器人能正常返回结果

---

## 🌐 部署选项

### 选项1：云服务器部署（推荐）

**优点**：稳定、可控、支持HTTPS
**服务商**：阿里云、腾讯云、华为云等

**步骤**：
1. 购买云服务器
2. 安装Python环境和依赖
3. 使用Gunicorn + Nginx部署
4. 配置SSL证书

### 选项2：Serverless部署

**优点**：无需维护服务器、按需付费
**平台**：阿里云函数计算、腾讯云SCF、华为云FunctionGraph

### 选项3：容器化部署

**优点**：易于扩展和管理
**工具**：Docker + Kubernetes

---

## 📝 示例：Docker部署

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
WORKDIR /app/src/api

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 构建和运行
```bash
# 构建镜像
docker build -t exhibition-api .

# 运行容器
docker run -d -p 8000:8000 exhibition-api
```

---

## 🔐 安全建议

1. **API认证**：添加API Key认证
2. **HTTPS加密**：确保数据传输安全
3. **速率限制**：防止API被滥用
4. **日志记录**：记录API调用日志便于排查
5. **错误处理**：友好的错误提示

---

## 📞 技术支持

如遇问题，请检查：
1. API服务是否正常运行
2. 网络连接是否正常
3. 请求参数是否正确
4. 查看API服务日志

---

## 📄 更新日志

### v1.0.0 (2025-03-25)
- ✅ 初始版本发布
- ✅ 支持展会信息查询
- ✅ 支持展商名录搜索
- ✅ 支持图片识别
- ✅ 支持Excel生成
- ✅ 支持企业微信AI+对接
