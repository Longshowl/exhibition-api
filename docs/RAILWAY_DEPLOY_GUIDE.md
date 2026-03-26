# Railway免费部署指南 - 10分钟完成

## ✅ 准备工作

- [x] GitHub账号（你已有）
- [x] 项目代码已准备
- [ ] 创建GitHub仓库（下一步）

---

## 📋 完整部署流程

### 第一步：创建GitHub仓库（5分钟）

#### 1. 访问GitHub创建仓库

1. 打开浏览器，访问：https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `exhibition-api` （或你喜欢的名字）
   - **Description**: `展会信息查询助手API服务`
   - **Visibility**: ✅ Public（公开，Railway免费版需要公开仓库）
   - ⚠️ **不要勾选** "Add a README file"
   - ⚠️ **不要勾选** "Add .gitignore"
   - ⚠️ **不要勾选** "Choose a license"
3. 点击 **Create repository**

#### 2. 推送代码到GitHub

创建仓库后，GitHub会显示一些命令，**忽略它们**，直接按照下面的步骤操作：

在项目根目录执行：

```bash
# 1. 添加远程仓库（替换为你的GitHub用户名）
git remote add origin https://github.com/你的用户名/exhibition-api.git

# 2. 推送代码到GitHub
git branch -M main
git push -u origin main
```

**示例：**
如果你的GitHub用户名是 `zhangsan`，仓库叫 `exhibition-api`：
```bash
git remote add origin https://github.com/zhangsan/exhibition-api.git
git branch -M main
git push -u origin main
```

#### 3. 验证代码已上传

访问你的仓库页面：`https://github.com/你的用户名/exhibition-api`

应该能看到所有代码文件。

---

### 第二步：部署到Railway（5分钟）

#### 1. 登录Railway

1. 访问：https://railway.app/
2. 点击右上角 **Login**
3. 选择 **Login with GitHub**
4. 授权Railway访问你的GitHub账号

#### 2. 创建新项目

1. 点击 **Dashboard** → **New Project**
2. 选择 **Deploy from GitHub repo**
3. 找到并选择 `exhibition-api` 仓库
4. 点击 **Configure** 按钮

#### 3. 配置项目

在配置页面设置：

- **Root Directory**: 输入 `src/api` （⚠️ 重要！不要填错）
- **Build Command**: 留空（自动检测）
- **Start Command**: 留空（从Procfile自动读取）

**关键步骤：**

1. 点击 **Variables** 标签
2. 添加环境变量（如果需要）：
   - `PYTHON_VERSION` = `3.9` （可选）

3. 点击 **Deploy** 按钮

#### 4. 等待部署完成

- Railway会自动：
  - 检测到Python项目
  - 安装requirements.txt中的依赖
  - 使用Procfile启动服务
- 部署时间：约2-3分钟

#### 5. 查看部署日志

- 点击项目名称进入详情页
- 点击 **Deployments** 标签
- 点击最新的部署查看日志
- 看到 `Uvicorn running on http://0.0.0.0:xxxx` 表示成功

---

### 第三步：配置域名（2分钟）

#### 1. 生成域名

1. 在项目详情页，点击 **Settings** 标签
2. 滚动到 **Domains** 部分
3. 点击 **Generate Domain**
4. Railway会自动生成一个域名，如：
   ```
   exhibition-api-production.up.railway.app
   ```

#### 2. 测试API

在浏览器或终端测试：

```bash
# 测试健康检查
curl https://你的域名.up.railway.app/health

# 应该返回
{"status": "healthy"}

# 测试展会查询
curl -X POST https://你的域名.up.railway.app/api/search_exhibition \
  -H "Content-Type: application/json" \
  -d '{"exhibition_name": "广交会"}'
```

#### 3. 查看API文档

打开浏览器访问：
```
https://你的域名.up.railway.app/docs
```

可以看到完整的API文档（Swagger UI）

---

## 🎉 部署成功！

### 你现在拥有：

1. **API地址**: `https://你的域名.up.railway.app`
2. **API文档**: `https://你的域名.up.railway.app/docs`
3. **自动HTTPS**: 已配置
4. **免费使用**: 每月$5免费额度，足够测试和小规模使用

### API端点：

- `GET /` - 服务信息
- `GET /health` - 健康检查
- `POST /api/chat` - 智能对话
- `POST /api/search_exhibition` - 查询展会
- `POST /api/search_exhibitors` - 搜索展商
- `POST /api/generate_excel` - 生成Excel

---

## 🔄 后续操作

### 更新代码

每次修改代码后：

```bash
# 1. 提交更改
git add .
git commit -m "更新说明"
git push

# 2. Railway会自动检测并重新部署
```

### 查看运行状态

1. 访问Railway Dashboard
2. 点击项目查看实时日志
3. 监控资源使用情况

### 设置环境变量（如果需要）

在Railway项目的 **Variables** 标签中添加：
- 点击 **New Variable**
- 输入变量名和值
- Railway会自动重启服务

---

## 🔗 企业微信对接配置

部署成功后，在企业微信AI+平台配置：

1. **API地址**: 填入你的Railway域名
   ```
   https://你的域名.up.railway.app/api/chat
   ```

2. **请求方法**: POST

3. **请求头**:
   ```
   Content-Type: application/json
   ```

4. **超时时间**: 30秒

---

## ⚠️ 注意事项

### Railway免费额度

- 每月$5免费额度
- 展会查询API使用量不大的话，免费额度完全够用
- 查看用量：Railway Dashboard → 项目 → Usage

### 服务休眠

免费版服务如果长时间无访问会休眠：
- 首次访问可能需要等待10-20秒唤醒
- 之后访问会很快
- 如需避免休眠，可考虑付费计划（$5/月起）

### 公开仓库

Railway免费版要求仓库必须公开：
- 代码不包含敏感信息即可
- 公司内部使用的API没问题

---

## 📞 常见问题

### Q1: 推送到GitHub失败？

**错误**: `remote: Repository not found`

**解决**: 确保仓库地址正确，格式为：
```bash
git remote set-url origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

### Q2: Railway部署失败？

**查看日志**:
1. Railway Dashboard → 项目 → Deployments
2. 点击失败的部署查看详细日志
3. 常见原因：
   - Root Directory 设置错误
   - requirements.txt 缺少依赖
   - Procfile 格式错误

### Q3: API访问超时？

首次访问可能需要唤醒服务，等待10-20秒再试。

### Q4: 如何添加团队成员？

Railway项目设置 → Members → 邀请GitHub用户

---

## 🎯 快速命令总结

```bash
# 1. 创建GitHub仓库并推送
git remote add origin https://github.com/你的用户名/exhibition-api.git
git branch -M main
git push -u origin main

# 2. Railway部署
# - 访问 railway.app
# - 登录GitHub
# - 创建项目，选择仓库
# - 设置 Root Directory: src/api
# - 点击 Deploy

# 3. 测试API
curl https://你的域名.up.railway.app/health
```

---

## ✅ 部署检查清单

- [ ] GitHub仓库已创建
- [ ] 代码已推送到GitHub
- [ ] Railway账号已登录
- [ ] 项目已在Railway创建
- [ ] Root Directory已设置为 `src/api`
- [ ] 部署成功
- [ ] 域名已生成
- [ ] API测试通过
- [ ] API文档可访问

---

祝部署顺利！🚀
