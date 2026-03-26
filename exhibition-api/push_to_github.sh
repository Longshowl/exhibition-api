#!/bin/bash

echo "=========================================="
echo "推送代码到GitHub仓库"
echo "=========================================="
echo ""
echo "仓库地址: https://github.com/Longshowl/exhibition-api"
echo ""

# 添加远程仓库
git remote add origin https://github.com/Longshowl/exhibition-api.git 2>/dev/null || git remote set-url origin https://github.com/Longshowl/exhibition-api.git

# 设置主分支
git branch -M main

# 推送代码
echo "正在推送代码到GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "访问你的仓库: https://github.com/Longshowl/exhibition-api"
    echo ""
    echo "下一步: 部署到Railway"
    echo "1. 访问: https://railway.app/"
    echo "2. 点击 Login with GitHub"
    echo "3. 创建新项目，选择 exhibition-api 仓库"
    echo "4. 设置 Root Directory: src/api"
    echo "5. 点击 Deploy"
else
    echo ""
    echo "❌ 推送失败，请检查GitHub认证"
    echo ""
    echo "可能的原因:"
    echo "1. 需要GitHub Personal Access Token认证"
    echo "2. 网络连接问题"
    echo ""
    echo "解决方案:"
    echo "1. 使用 GitHub CLI: gh auth login"
    echo "2. 或使用 SSH: git remote set-url origin git@github.com:Longshowl/exhibition-api.git"
fi
