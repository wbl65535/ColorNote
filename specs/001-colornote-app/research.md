# Research & Technology Decisions

**Feature**: ColorNote - 全栈便利贴应用
**Date**: 2025-12-23
**Status**: Complete

## Technology Stack Decisions

### Backend Framework: Flask 3.0 + Python 3.11

**Decision**: 采用 Flask 3.0 作为 Web 框架，配合 Python 3.11。

**Rationale**:
- 符合宪法要求：必须使用 Python 3.11+ 和支持 Serverless 部署的 Web 框架
- Flask 轻量级，适合单体应用架构
- 良好的扩展性和社区支持
- Vercel 对 Flask 应用有完善的支持

**Alternatives Considered**:
- FastAPI: 虽然性能更好，但学习曲线陡峭，Serverless 部署复杂度较高
- Django: 过于重量级，适合大型应用，不符合轻量级需求

### ORM: SQLAlchemy

**Decision**: 使用 SQLAlchemy 作为数据库 ORM。

**Rationale**:
- 与 Flask 生态完美集成 (Flask-SQLAlchemy)
- 支持复杂查询和关系映射
- 良好的事务管理和连接池支持
- 社区成熟，文档完善

**Alternatives Considered**:
- Peewee: 轻量但功能有限，不适合复杂业务逻辑
- 原生 SQL: 维护成本高，容易出错

### Frontend Framework: Vue.js 3 (CDN)

**Decision**: 使用 Vue.js 3 通过 CDN 引入。

**Rationale**:
- 符合宪法要求：现代前端框架，支持 CDN 引入
- Vue.js 3 提供了 Composition API，更好的 TypeScript 支持
- CDN 引入减少打包体积，适合移动端优化
- 响应式数据绑定适合动态内容更新

**Alternatives Considered**:
- React: 虽然功能强大，但 CDN 引入的版本相对复杂
- 原生 JavaScript: 开发效率低，维护困难

### Styling: Tailwind CSS (CDN)

**Decision**: 使用 Tailwind CSS 通过 CDN 引入。

**Rationale**:
- 符合移动端响应式设计要求
- 原子化 CSS 理念，减少自定义样式代码
- CDN 引入减少应用体积
- 移动端优先的设计理念

**Alternatives Considered**:
- Bootstrap: 虽然成熟，但样式相对固定，不够灵活
- 自定义 CSS: 开发和维护成本高

### Database: TiDB Cloud

**Decision**: 使用 TiDB Cloud 作为数据库服务。

**Rationale**:
- 符合宪法要求：云数据库服务，MySQL 兼容，支持 JSON 字段
- 分布式架构，良好的扩展性
- Serverless 友好，无需管理服务器
- 支持 JSON 字段类型，适合存储图片 URL 数组

**Alternatives Considered**:
- PlanetScale: 虽然优秀，但价格相对较高
- AWS RDS: 配置复杂，不够轻量

### Storage: Vercel Blob

**Decision**: 使用 Vercel Blob 作为图片存储服务。

**Rationale**:
- 符合宪法要求：云存储服务，禁止 base64 格式存入数据库
- 与 Vercel 生态完美集成
- 全球 CDN 加速，保证访问速度
- 安全可靠，自动备份

**Alternatives Considered**:
- AWS S3: 虽然功能强大，但配置相对复杂
- Cloudinary: 适合图片处理，但成本较高

### Testing Frameworks

**Decision**:
- API/单元测试：pytest
- E2E 测试：Playwright

**Rationale**:
- 符合宪法要求：包含 E2E 和 API 测试框架
- pytest: Python 生态标准，简单易用
- Playwright: 支持多种浏览器，测试移动端友好
- 两者结合提供完整的测试覆盖

**Alternatives Considered**:
- unittest: Python 标准库，但不够现代化
- Selenium: 虽然经典，但维护成本高

### Deployment: Vercel Serverless Functions

**Decision**: 使用 Vercel Serverless Functions 进行部署。

**Rationale**:
- 符合宪法要求：Serverless Functions 架构，本地环境与生产环境一致
- Vercel CLI 提供本地开发支持 (`vercel dev`)
- 自动扩缩容，成本优化
- 内置 CDN 和边缘计算

**Alternatives Considered**:
- AWS Lambda: 虽然强大，但配置复杂，学习成本高
- Heroku: 部署简单但成本较高

## Architecture Decisions

### Monolithic Architecture with SPA Frontend

**Decision**: 采用 Flask 单体应用 + Vue.js SPA 的架构模式。

**Rationale**:
- 应用规模适中，单体架构复杂度可控
- 前后端分离，但部署在一起简化运维
- Vue.js 提供丰富的交互体验
- 符合 Serverless 部署要求

**Alternatives Considered**:
- 微服务架构: 过度设计，增加复杂度
- 纯后端渲染: 用户体验不如 SPA

### Data Model Design

**Decision**: 单表设计 (notes)，使用 JSON 字段存储图片 URL 数组。

**Rationale**:
- 符合宪法要求：支持 JSON 字段类型
- 简化数据模型，减少关联查询
- TiDB 支持 JSON 操作，性能良好
- 符合业务需求：笔记为主要实体，图片为附属

**Alternatives Considered**:
- 图片单独建表: 增加查询复杂度，不必要

## Performance & Scalability Considerations

### Mobile Optimization

**Decision**: 专门针对移动端竖屏进行优化。

**Rationale**:
- 符合宪法要求：移动端体验目标明确
- 目标用户主要在手机上使用
- 触控交互优化，可点击区域 ≥44px
- 竖屏布局优先

### Cold Start Handling

**Decision**: 通过 UI 反馈和优化包体积来处理 Serverless 冷启动。

**Rationale**:
- Vercel Serverless 冷启动不可避免
- UI 上提供明确加载反馈
- CDN 引入减少应用体积
- 缓存策略优化首次加载

## Security Considerations

### Image Upload Security

**Decision**: 文件类型和大小限制 + 服务端验证。

**Rationale**:
- 只允许图片格式上传
- 限制单张图片 5MB
- 服务端重新验证文件类型
- Vercel Blob 提供安全保障

### Data Validation

**Decision**: 前后端双重验证 + 数据库约束。

**Rationale**:
- 前端提供即时反馈
- 后端保证数据完整性
- 数据库约束防止非法数据
- 多层防护确保安全性

## Development Workflow

### Local Development

**Decision**: 使用 `vercel dev` 统一开发环境。

**Rationale**:
- 符合宪法要求：本地环境与生产环境一致
- Vercel CLI 提供完整模拟环境
- 简化开发和调试流程

### CI/CD Pipeline

**Decision**: GitHub Actions + Vercel 自动部署。

**Rationale**:
- 测试先行：先运行测试，再部署
- 自动化保证一致性
- 快速反馈和部署

## Summary

所有技术决策均符合宪法原则，技术选型考虑了：
- 开发效率和维护成本
- 性能和用户体验
- Serverless 部署的特殊要求
- 移动端优化需求

技术栈成熟稳定，社区支持良好，为项目成功奠定坚实基础。
