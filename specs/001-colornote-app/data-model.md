# Data Model Design

**Feature**: ColorNote - 全栈便利贴应用
**Date**: 2025-12-23

## Entity Overview

基于功能需求分析，ColorNote 应用的核心实体为便签 (Note)，图片作为便签的附属属性存储在便签实体中。

## Note Entity

### Database Schema

**Table Name**: `notes`

| 字段名     | 类型     | 约束                         | 说明          |
| ---------- | -------- | ---------------------------- | ------------- |
| id         | INTEGER  | 主键，自增                   | 唯一标识      |
| title      | VARCHAR  | ≤30字符，非空                 | 标题          |
| content    | TEXT     | ≤500字符，非空                | 内容          |
| color      | VARCHAR  | 长度7，非空，默认 `#FFE57F`   | HEX 颜色值    |
| image_urls | JSON     | 可为空，最多3个URL            | 图片URL数组   |
| created_at | DATETIME | 默认 NOW()                   | 创建时间      |
| updated_at | DATETIME | 默认 NOW()，更新时自动刷新    | 更新时间      |

### Field Constraints & Validation Rules

#### Title Field
- **Type**: VARCHAR(30)
- **Constraints**: NOT NULL, LENGTH ≤ 30
- **Validation**: 前端实时校验，超过30字符禁止输入
- **Default**: N/A

#### Content Field
- **Type**: TEXT (supports up to 500 characters)
- **Constraints**: NOT NULL, LENGTH ≤ 500
- **Validation**: 前端实时校验，超过500字符禁止输入
- **Default**: N/A

#### Color Field
- **Type**: VARCHAR(7)
- **Constraints**: NOT NULL, VALID HEX COLOR
- **Validation**: 必须是有效的HEX颜色值 (格式: #RRGGBB)
- **Default**: `#FFE57F` (黄色)
- **Allowed Values**:
  - `#FFE57F` (Yellow)
  - `#FFB3BA` (Pink)
  - `#BAE1FF` (Blue)
  - `#BAFFC9` (Green)
  - `#E0BBE4` (Purple)
  - `#FFDAC1` (Orange)

#### Image URLs Field
- **Type**: JSON ARRAY
- **Constraints**: 可为空，数组长度 ≤ 3
- **Validation**:
  - 每个URL必须是有效的Vercel Blob URL
  - URL格式: `https://{project}.vercel-storage.com/notes/{note_id}/{timestamp}_{filename}`
- **Default**: NULL

#### Timestamp Fields
- **created_at**: 记录首次创建时间，自动设置
- **updated_at**: 记录最后修改时间，更新操作时自动刷新

### Business Rules

#### Note Creation
- 所有字段均为必填（color 有默认值）
- 创建时自动设置 created_at 和 updated_at
- image_urls 初始为空数组或null

#### Note Update
- 允许修改 title, content, color, image_urls
- 更新时自动刷新 updated_at
- id 和 created_at 不可修改

#### Note Deletion
- 物理删除记录
- 同时删除关联的图片文件（从 Vercel Blob 删除）

#### Image Management
- 每个笔记最多3张图片
- 图片存储在 Vercel Blob，不在数据库中存储二进制数据
- 数据库仅存储图片的访问URL

### SQLAlchemy Model Definition

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func

class Note(db.Model):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30), nullable=False)
    content = Column(Text, nullable=False)
    color = Column(String(7), nullable=False, default='#FFE57F')
    image_urls = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<Note {self.id}: {self.title}>'
```

### Data Relationships

- **Note**: 根实体，无外键依赖
- **Images**: 通过 image_urls JSON 字段关联，不使用传统外键关系
- **Users**: 单用户应用，无用户实体（可后续扩展）

### Indexing Strategy

#### Primary Key
- `id` 字段自动建立主键索引

#### Performance Indexes (Recommended)
```sql
-- 按创建时间降序查询索引（主要查询模式）
CREATE INDEX idx_notes_created_at ON notes (created_at DESC);

-- 按更新时间降序查询索引（备用）
CREATE INDEX idx_notes_updated_at ON notes (updated_at DESC);
```

### Data Migration Strategy

#### Initial Schema
```sql
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

#### Future Migrations
- 版本化迁移脚本存储在 `migrations/` 目录
- 使用 Alembic 或 Flask-Migrate 管理
- 支持回滚和数据迁移

### Data Integrity

#### Database Constraints
- NOT NULL 约束确保必需字段
- CHECK 约束验证颜色格式（如果数据库支持）
- 外键约束：无（单实体设计）

#### Application-Level Validation
- 字段长度验证
- 数据类型验证
- 业务规则验证（如图片数量限制）
- 图片URL格式验证

### Performance Considerations

#### Query Patterns
1. **List Notes**: `SELECT * FROM notes ORDER BY created_at DESC`
2. **Get Note**: `SELECT * FROM notes WHERE id = ?`
3. **Create Note**: `INSERT INTO notes (...) VALUES (...)`
4. **Update Note**: `UPDATE notes SET ... WHERE id = ?`
5. **Delete Note**: `DELETE FROM notes WHERE id = ?`

#### Optimization Strategies
- 索引优化主要查询（按时间排序）
- 连接池配置（SQLAlchemy 默认提供）
- 读写分离（未来扩展考虑）

### Security Considerations

#### Data Sanitization
- 防止SQL注入：使用ORM参数化查询
- XSS防护：前端数据转义，后端输入验证
- 数据验证：多层验证（前端 + 后端 + 数据库）

#### Access Control
- 单用户应用，无复杂权限控制
- API密钥保护（Vercel Blob 访问）
- HTTPS强制使用

### Monitoring & Observability

#### Key Metrics
- 笔记数量统计
- 平均图片数量
- 数据库查询性能
- 存储使用情况

#### Logging
- 创建/更新/删除操作日志
- 错误日志记录
- 性能监控日志
