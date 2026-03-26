#!/bin/bash

# 展会信息查询助手 - API服务启动脚本

echo "========================================="
echo "展会信息查询助手 - API服务"
echo "========================================="
echo ""

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "错误: 未找到Python环境"
    exit 1
fi

echo "Python版本: $(python --version)"
echo ""

# 进入API目录
cd src/api

# 启动服务
echo "正在启动API服务..."
echo "服务地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo "========================================="
echo ""

python main.py
