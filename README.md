# ColorNote - 全栈便利贴应用

一个针对移动端竖屏优化的彩色便利贴单页应用，提供创建、浏览、编辑、删除笔记的核心能力。

## 🚀 快速开始

### 在线演示
[ColorNote 应用](https://colornote.vercel.app)

### 本地开发

1. **克隆项目**
   ```bash
   git clone https://github.com/wbl65535/ColorNote.git
   cd ColorNote
   ```

2. **环境配置**
   ```bash
   # 复制环境变量模板
   cp env.example .env

   # 编辑环境变量
   # DB_HOST=your-tidb-host
   # DB_USERNAME=your-username
   # DB_PASSWORD=your-password
   # DB_DATABASE=colornote
   # BLOB_READ_WRITE_TOKEN=your-vercel-blob-token
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行开发服务器**
   ```bash
   # 使用 Vercel CLI (推荐)
   vercel dev

   # 或直接使用 Flask
   python main.py
   ```

5. **访问应用**
   打开浏览器访问 `http://localhost:3000`

## 📱 功能特性

### 核心功能
- ✅ **创建笔记** - 滑动面板创建，标题和内容输入
- ✅ **查看列表** - 按时间倒序显示，内容预览
- ✅ **编辑笔记** - 点击编辑，修改标题、内容、颜色
- ✅ **删除笔记** - 确认对话框删除功能
- ✅ **颜色主题** - 6种预设颜色选择
- ✅ **图片上传** - 支持最多3张图片，Vercel Blob存储

### 技术特性
- 📱 **移动端优化** - 响应式设计，触控友好
- 🎨 **现代化UI** - Vue.js + Tailwind CSS
- ⚡ **高性能** - 快速加载，流畅交互
- 🔒 **数据持久化** - TiDB云数据库
- ☁️ **云存储** - Vercel Blob图片存储
- 🧪 **完整测试** - API和E2E测试覆盖

## 🏗️ 技术栈

### 后端
- **Python 3.11**
- **Flask 3.0** - Web框架
- **SQLAlchemy** - ORM
- **TiDB Cloud** - MySQL兼容数据库

### 前端
- **Vue.js 3** - 响应式框架
- **Tailwind CSS** - 实用优先CSS框架

### 存储与部署
- **Vercel Blob** - 云对象存储
- **Vercel Functions** - Serverless部署

### 测试
- **pytest** - API单元测试
- **Playwright** - E2E端到端测试

## 🗂️ 项目结构

```
ColorNote/
├── app/                          # Flask应用
│   ├── __init__.py              # 应用工厂
│   ├── config.py                # 配置管理
│   ├── models.py                # 数据模型
│   ├── repositories.py          # 数据访问层
│   ├── routes.py                # API路由
│   ├── services.py              # 业务逻辑
│   ├── templates/
│   │   └── index.html           # 主页面模板
│   └── static/
│       ├── js/app.js            # Vue.js逻辑
│       └── css/custom.css       # 自定义样式
├── api/                         # Vercel API
│   └── index.py                 # Vercel入口点
├── tests/                       # 测试套件
│   ├── api/                     # API测试
│   ├── e2e/                     # E2E测试
│   └── conftest.py              # 测试配置
├── specs/                       # 规范文档
├── vercel.json                  # Vercel配置
├── requirements.txt             # Python依赖
└── README.md                    # 项目文档
```

## 🧪 运行测试

### API测试
```bash
pytest tests/api/ -v
```

### E2E测试
```bash
# 确保开发服务器运行在后台
vercel dev &

# 运行E2E测试
pytest tests/e2e/ -v
```

### 所有测试
```bash
pytest tests/ -v
```

## 🚀 部署到Vercel

### 自动部署 (推荐)
项目已配置GitHub集成，推送到main分支自动部署。

### 手动部署
```bash
# 安装Vercel CLI
npm install -g vercel

# 登录Vercel
vercel login

# 部署
vercel

# 生产部署
vercel --prod
```

## 🔧 环境变量配置

在Vercel Dashboard或本地.env文件中配置：

```bash
# 数据库配置
DB_HOST=your-tidb-host
DB_PORT=4000
DB_USERNAME=your-username
DB_PASSWORD=your-password
DB_DATABASE=colornote
DB_TEST_DATABASE=colornote_test

# Vercel Blob存储
BLOB_READ_WRITE_TOKEN=your-blob-token

# Flask配置
FLASK_ENV=production
SECRET_KEY=your-secret-key
```

## 📊 性能指标

- **首屏加载**: < 2秒 (P95)
- **交互响应**: < 300ms (P95)
- **图片上传成功率**: > 95%
- **移动端兼容**: iPhone 15+ / Android主流机型

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

项目维护者: [wbl65535](https://github.com/wbl65535)

项目链接: [https://github.com/wbl65535/ColorNote](https://github.com/wbl65535/ColorNote)

---

**ColorNote** - 让记录想法变得简单而美丽 ✨