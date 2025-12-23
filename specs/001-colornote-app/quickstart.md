# ColorNote 开发快速开始指南

**Feature**: ColorNote - 全栈便利贴应用
**Date**: 2025-12-23

## 环境准备

### 系统要求

- **Python**: 3.11 或更高版本
- **Node.js**: 18+ (用于 Vercel CLI)
- **Git**: 2.30+
- **操作系统**: Windows 10+ / macOS 12+ / Ubuntu 20.04+

### 必需工具

1. **Python 3.11+**
   ```bash
   # Windows (使用 winget)
   winget install Python.Python.3.11

   # macOS (使用 Homebrew)
   brew install python@3.11

   # Ubuntu
   sudo apt update
   sudo apt install python3.11 python3.11-venv
   ```

2. **Vercel CLI**
   ```bash
   npm install -g vercel
   # 或使用其他包管理器
   yarn global add vercel
   ```

3. **Git**
   ```bash
   # Windows
   winget install Git.Git

   # macOS
   brew install git

   # Ubuntu
   sudo apt install git
   ```

## 项目设置

### 1. 克隆项目

```bash
git clone https://github.com/wbl65535/ColorNote.git
cd ColorNote
```

### 2. 切换到功能分支

```bash
git checkout 001-colornote-app
```

### 3. 创建 Python 虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 4. 安装 Python 依赖

```bash
pip install -r scripts/requirements.txt
```

**requirements.txt 内容**:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
python-dotenv==1.0.0
vercel-blob==0.1.0  # 如果可用，否则使用 requests + Vercel API
```

### 5. 环境变量配置

创建 `.env` 文件：

```bash
# 数据库配置 (TiDB Cloud)
DB_HOST=your-tidb-host
DB_PORT=4000
DB_DATABASE=colornote
DB_TEST_DATABASE=colornote_test
DB_USERNAME=your-username
DB_PASSWORD=your-password

# Vercel Blob 配置
BLOB_READ_WRITE_TOKEN=your-blob-token
```

### 6. 获取 Vercel Blob Token

```bash
# 方法1: 使用 Vercel CLI (推荐)
vercel env pull .env.local
# 或直接拉取到 .env
vercel env pull .env

# 方法2: 从 Vercel Dashboard 获取
# 1. 访问 https://vercel.com/dashboard
# 2. 选择你的项目
# 3. 进入 Settings > Environment Variables
# 4. 复制 BLOB_READ_WRITE_TOKEN 的值
```

### 7. 数据库初始化

确保 TiDB 数据库已创建所需的数据库和表：

```sql
-- 创建数据库
CREATE DATABASE colornote;
CREATE DATABASE colornote_test;

-- 使用数据库
USE colornote;

-- 创建表 (详见 data-model.md)
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(30) NOT NULL,
    content TEXT NOT NULL,
    color VARCHAR(7) NOT NULL DEFAULT '#FFE57F',
    image_urls JSON NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 本地开发

### 启动开发服务器

```bash
# 使用 Vercel CLI 启动 (推荐)
vercel dev

# 或直接使用 Flask (仅用于测试，不推荐日常使用)
flask run
```

服务器将在 `http://localhost:3000` 启动。

### 验证安装

1. **打开浏览器**访问 `http://localhost:3000`
2. **检查控制台**确认无错误
3. **测试基本功能**：
   - 创建新笔记
   - 查看笔记列表
   - 编辑现有笔记

## 开发工作流

### 代码结构

```
app/
├── __init__.py          # Flask 应用初始化
├── models.py            # 数据模型
├── repositories.py      # 数据访问层
├── routes.py            # API 路由
├── services.py          # 业务逻辑
├── config.py            # 配置管理
├── templates/
│   └── index.html       # 主页面模板
└── static/
    ├── js/
    │   └── app.js       # Vue.js 前端逻辑
    └── css/
        └── custom.css   # 自定义样式

tests/
├── conftest.py          # 测试配置
├── api/                 # API 测试
└── e2e/                 # E2E 测试
```

### 常用命令

```bash
# 运行所有测试
pytest

# 运行 API 测试
pytest tests/api/

# 运行 E2E 测试
pytest tests/e2e/

# 格式化代码
black app/ tests/

# 检查代码质量
flake8 app/ tests/

# 启动本地开发服务器
vercel dev
```

### 调试技巧

1. **Flask 调试模式**：
   ```python
   app.config['DEBUG'] = True
   ```

2. **浏览器开发者工具**：
   - Network 标签页查看 API 请求
   - Console 标签页查看前端错误
   - Application 标签页查看本地存储

3. **数据库调试**：
   ```python
   # 在 routes.py 中添加调试日志
   print(f"Query result: {notes}")
   ```

## 测试策略

### API 测试

```bash
# 运行 API 单元测试
pytest tests/api/test_api_routes.py -v

# 测试特定端点
pytest tests/api/test_api_routes.py::test_create_note -v
```

### E2E 测试

```bash
# 运行 E2E 测试 (需要 vercel dev 在后台运行)
pytest tests/e2e/ -v

# 测试特定用户流程
pytest tests/e2e/test_crud_operations.py -v
```

### 测试数据

测试使用独立的数据库 `colornote_test`，测试后自动清理数据。

## 部署流程

### 开发环境部署

```bash
# 登录 Vercel
vercel login

# 链接项目
vercel link

# 部署到预览环境
vercel

# 部署到生产环境
vercel --prod
```

### CI/CD

项目使用 GitHub Actions 进行自动化部署：

1. **Push 到 main 分支** → 自动部署到生产环境
2. **Pull Request** → 自动部署到预览环境
3. **测试失败** → 阻止合并和部署

## 故障排除

### 常见问题

#### 1. Vercel Dev 启动失败

**问题**: `vercel dev` 命令失败
**解决**:
```bash
# 检查 Vercel CLI 安装
vercel --version

# 重新安装 Vercel CLI
npm install -g vercel

# 检查项目配置
vercel link
```

#### 2. 数据库连接失败

**问题**: 无法连接到 TiDB
**解决**:
```bash
# 检查环境变量
echo $DB_HOST
echo $DB_DATABASE

# 测试数据库连接
python -c "
import os
from sqlalchemy import create_engine
engine = create_engine(f'mysql://{os.getenv(\"DB_USERNAME\")}:{os.getenv(\"DB_PASSWORD\")}@{os.getenv(\"DB_HOST\")}:{os.getenv(\"DB_PORT\")}/{os.getenv(\"DB_DATABASE\")}')
engine.connect()
print('Database connection successful')
"
```

#### 3. 图片上传失败

**问题**: Vercel Blob 上传失败
**解决**:
```bash
# 检查 BLOB_READ_WRITE_TOKEN
echo $BLOB_READ_WRITE_TOKEN

# 从 Vercel 拉取最新环境变量
vercel env pull .env.local

# 检查 token 权限
curl -H "Authorization: Bearer $BLOB_READ_WRITE_TOKEN" \
     https://blob.vercel-storage.com
```

#### 4. 前端资源不加载

**问题**: Vue.js 或 Tailwind CSS 不工作
**解决**:
```html
<!-- 检查 index.html 中的 CDN 链接 -->
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
<link href="https://cdn.tailwindcss.com" rel="stylesheet">
```

### 获取帮助

- **查看日志**: `vercel logs`
- **检查环境变量**: `vercel env ls`
- **重置本地环境**: 删除 `node_modules` 和 `.vercel`，重新安装

## 下一步

1. **完成基础 CRUD 功能**实现
2. **添加图片上传功能**
3. **实现响应式设计优化**
4. **编写完整的测试套件**
5. **性能优化和监控**

按照 `/speckit.tasks` 命令生成的详细任务列表逐步实施。
