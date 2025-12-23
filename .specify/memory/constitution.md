<!--
Sync Impact Report:
Version change: N/A → 1.0.0
List of modified principles: N/A (initial creation)
Added sections: All sections (initial constitution)
Removed sections: None
Templates requiring updates: ✅ checked - spec-template.md, spec-template-rendered.md, plan-template.md, tasks-template.md (no updates needed)
Follow-up TODOs: None
-->

# ColorNote - Constitution

**Version**: 1.0.0
**Ratified**: 2025-12-23
**Last Amended**: 2025-12-23

## Project Identity

**Project Name**: ColorNote - 全栈便利贴应用

**Repository**: https://github.com/wbl65535/ColorNote
**Default Branch**: main

**Guardrail**: Implementation must use the above repository and branch naming; generation of inconsistent repository names, remotes, or default branches is prohibited.

## Project Description and Scope

**Description**: 一个针对移动端竖屏优化的彩色便利贴单页应用（SPA），提供创建、浏览、编辑、删除笔记的核心能力，并保证在本地 `vercel dev` 与 Vercel 生产环境行为一致。

**Target Users**: 需要在手机浏览器里快速记录想法、待办事项的个人用户，以竖屏使用为主。

**Scope**:

- **Included**: 创建、编辑、删除便利贴；6 种预设颜色主题；列表展示与内容预览；图片上传与展示；数据持久化（云数据库 + 云存储）。
- **Excluded**: 用户登录/账户系统；多设备同步；分享/协同编辑；富文本编辑（仅纯文本）。

## Technical Stack Principles

- **Backend**: 必须使用 Python 3.11+，Web 框架需支持 Serverless 部署。
- **Frontend**: 必须使用现代前端框架（支持 CDN 引入），必须支持移动端响应式设计。
- **Database**: 必须使用云数据库服务（MySQL 兼容），支持 JSON 字段类型。
- **Storage**: 图片必须存储在云存储服务中，禁止将图片数据以 base64 格式存入数据库。
- **Testing**: 必须包含端到端测试（E2E）和 API 测试框架。
- **Deployment**: 必须使用 Serverless Functions 架构，本地开发环境必须与生产环境一致。
- **Development Tools**: 必须使用 Vercel CLI 进行本地开发与部署。

## Quality and Delivery Guardrails

- 核心 CRUD 流程必须具备端到端测试覆盖（创建、读取、更新、删除）。
- 本地 `vercel dev` 与 Vercel 生产环境行为必须一致。
- 移动端体验目标：首屏加载时间 < 2 秒，交互响应时间（点击到 UI 反馈）< 300ms（P95）。

## Governance

### Amendment Procedure

宪法修改需要项目主要贡献者一致同意。修改提案应在GitHub Issues中提出，并经过代码审查流程。重大修改（涉及技术栈变更或项目范围调整）需要至少一周的讨论期。

### Versioning Policy

宪法版本遵循语义化版本控制：
- MAJOR: 向后不兼容的治理原则移除或重新定义
- MINOR: 新原则/章节添加或现有指导的重大扩展
- PATCH: 澄清、措辞修改、拼写错误修复、非语义性完善

### Compliance Review

所有代码变更必须通过宪法一致性检查。项目维护者负责确保实现与宪法原则保持一致。违反宪法的代码变更将被拒绝合并。