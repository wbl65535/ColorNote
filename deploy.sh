#!/bin/bash

# ColorNote 部署脚本
# 用于Vercel部署和环境配置

set -e

echo "🚀 开始部署 ColorNote..."

# 检查Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI 未安装，请运行: npm install -g vercel"
    exit 1
fi

# 检查是否已登录
if ! vercel whoami &> /dev/null; then
    echo "🔐 请先登录Vercel:"
    vercel login
fi

# 检查环境变量
echo "🔍 检查环境变量配置..."

# 检查数据库环境变量
required_vars=("DB_HOST" "DB_USERNAME" "DB_PASSWORD" "DB_DATABASE")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ] && [ ! -f ".env" ]; then
        echo "⚠️  环境变量 $var 未设置"
        echo "请在Vercel Dashboard中配置或创建.env文件"
    fi
done

# 检查Vercel Blob token
if [ -z "$BLOB_READ_WRITE_TOKEN" ] && [ ! -f ".env" ]; then
    echo "⚠️  BLOB_READ_WRITE_TOKEN 未设置"
    echo "请在Vercel Dashboard中配置Vercel Blob token"
fi

# 拉取最新环境变量
echo "📥 同步环境变量..."
vercel env pull .env.local 2>/dev/null || echo "无法拉取环境变量，请手动配置"

# 运行测试 (可选)
echo "🧪 运行测试..."
if command -v pytest &> /dev/null; then
    pytest tests/ -v --tb=short || echo "⚠️  测试失败，但继续部署"
else
    echo "⚠️  pytest 未安装，跳过测试"
fi

# 部署到预览环境
echo "🌐 部署到预览环境..."
vercel --yes

# 获取部署URL
deploy_url=$(vercel --yes 2>&1 | grep -o 'https://[^[:space:]]*')

if [ -n "$deploy_url" ]; then
    echo "✅ 部署成功!"
    echo "🌐 预览URL: $deploy_url"
    echo ""
    echo "💡 要部署到生产环境，请运行:"
    echo "   vercel --prod"
else
    echo "⚠️  无法获取部署URL，请检查Vercel日志"
fi

echo ""
echo "🎉 ColorNote 部署完成!"
echo "📖 查看完整文档: https://github.com/wbl65535/ColorNote"
