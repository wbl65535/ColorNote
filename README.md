# Spec-Kit 示例模板：ColorNote 项目

> **这是一个 Spec-Kit 示例模板仓库**，用于演示如何通过 Spec-Kit 进行规范驱动的项目开发。

本仓库提供了完整的 Spec-Kit 规范模板（Constitution / Specify / Plan），帮助你快速开始使用 Spec-Kit 进行 ColorNote 项目的开发。本 README 将指导你如何在自己的项目中使用这些模板文件。

## 🎯 项目目的

本仓库是一个**示例模板项目**，旨在：

- 提供**开箱即用**的完整规范模板（Constitution / Specify / Plan）
- 展示如何使用 Spec-Kit 进行规范驱动开发
- 演示如何通过 AI 助手与 Spec-Kit 协作进行开发
- 作为学习 Spec-Kit 的实践案例

### 核心价值

`spec-template.md` 中的三个章节**直接对应** Spec-Kit 的三个开发阶段：

1. **Constitution 章节** → `/speckit.constitution` 命令

   - 项目原则和开发指南
   - 技术栈约束原则和质量红线

2. **Specify 章节** → `/speckit.specify` 命令

   - 功能需求和验收标准
   - 描述"要做什么"和"如何验证"

3. **Plan 章节** → `/speckit.plan` 命令

   - 技术实现方案
   - 架构设计和实现细节

**你不需要从零开始写这些规范**，只需要：

1. 替换模板中的占位符
2. 将内容复制到相应的 Spec-Kit 命令中
3. 开始使用 Spec-Kit 进行开发

## 📋 如何使用本模板

1. **Fork 或 Clone 本仓库**，获取模板文件
2. **在 GitHub 上创建你的 ColorNote 项目仓库**（记录仓库 owner 和名称）
3. **填写 `project.config.json`**，填入你的项目信息：
   - `github_owner`：你的 GitHub 用户名或组织名
   - `repo_name`：你的项目仓库名称（必须与步骤 2 中创建的仓库名一致）
   - `default_branch`：默认分支名（通常是 `main`）
   - `vercel_project_name`：Vercel 项目名称（可选）
4. **手动初始化 Git 仓库**（删除模板仓库的 `.git/` 并重新初始化）：
   - **Windows (PowerShell)**：删除模板仓库的 Git 历史：`Remove-Item -Recurse -Force .git`
   - **macOS / Linux**：删除模板仓库的 Git 历史：`rm -rf .git`
   - 初始化 Git 仓库：`git init`
   - 设置默认分支：`git branch -M main`（或你配置的分支名）
   - 添加远程仓库：`git remote add origin https://github.com/your-username/ColorNote.git`（替换为你的仓库地址）
   - 验证配置：`git remote -v` 应该显示你的仓库地址
5. **在你的项目中初始化 Spec-Kit**：`specify init .`
6. **使用 AI 助手命令**，将 `spec-template.md` 中的内容复制到相应的 Spec-Kit 命令中
7. **开始使用 Spec-Kit 进行开发**

---

## 📁 模板文件说明

本仓库包含以下模板文件：

```text
.
├── env.example              # 环境变量模板（需复制为 .env 并填写）
├── project.config.json      # 项目配置（需填写你的项目信息）
├── spec-template.md         # Spec-Kit 三件套模板（包含占位符）
├── scripts/
│   ├── render-spec.py      # Python 脚本：使用 Jinja2 替换占位符（自动检查并安装依赖）
│   └── requirements.txt     # Python 依赖（Jinja2）
└── README.md               # 本文件
```

### 文件用途

- **`env.example`**：环境变量配置模板，包含数据库连接、应用环境等配置项
- **`project.config.json`**：项目元信息配置示例文件，包含以下用途：
  - 用于替换 `spec-template.md` 中的占位符
  - 在你的项目中，该文件会被 Preflight 校验读取（见 Plan 章节）
  - **注意**：模板仓库中的是示例，你需要在**自己的项目**中创建并填写该文件
- **`spec-template.md`**：包含 Constitution（项目宪章）、Specify（需求规格）、Plan（实现计划）三个章节的完整模板，包含占位符需要替换
- **`scripts/render-spec.py`**：Python 脚本，使用 Jinja2 模板引擎自动替换 `spec-template.md` 中的占位符，生成 `spec-template-rendered.md`。脚本会自动检查并安装依赖（Jinja2）
- **`scripts/requirements.txt`**：Python 依赖文件，包含 Jinja2（用于模板渲染）

---

## 🚀 使用流程

### 第一步：准备前置条件

在开始之前，请确保以下条件已满足：

#### 1. 安装 Spec-Kit CLI

```bash
# 使用 uv 安装（推荐）
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 验证安装
specify init --help
```

#### 2. 准备 GitHub 仓库并初始化项目

- **重要**：本仓库是模板示例，你需要创建**你自己的** ColorNote 项目仓库
- 在 GitHub 上创建目标仓库（可以命名为 `ColorNote` 或其他你喜欢的名称）
- 记录以下信息：
  - 仓库 owner（你的 GitHub 用户名或组织名）
  - 仓库名称（例如 `ColorNote`）
  - 默认分支名（通常是 `main`）

**手动初始化 Git 仓库**：

按照以下步骤手动初始化 Git 仓库。以下以 **Windows (PowerShell)** 为主要说明，macOS/Linux 用户请参考对应的命令。

1. **检查并删除模板仓库的 Git 历史**：

   **Windows (PowerShell)**：

   ```powershell
   # 检查当前 Git 配置
   git remote -v
   
   # 如果显示的是模板仓库地址（包含 Spec-Kit-Example-ColorNote），需要删除
   Remove-Item -Recurse -Force .git
   ```

   > **macOS / Linux (Bash / Zsh) 用户**：使用 `rm -rf .git` 代替 `Remove-Item -Recurse -Force .git`  
   > **注意**：如果 `git remote -v` 显示的是你自己的仓库地址，可以跳过删除步骤。

2. **初始化 Git 仓库**：

   **Windows (PowerShell)**：

   ```powershell
   git init
   ```

   > 注意：Git 命令在所有操作系统上都是相同的。macOS/Linux 用户使用相同的命令。

3. **设置默认分支**：

   **Windows (PowerShell)**：

   ```powershell
   # 使用你在 project.config.json 中配置的分支名（通常是 main）
   git branch -M main
   ```

   如果 `project.config.json` 中配置的是其他分支名（如 `master`），使用对应的分支名。

   > 注意：macOS/Linux 用户使用相同的命令。

4. **添加远程仓库**：

   **Windows (PowerShell)**：

   ```powershell
   # 替换为你的实际仓库地址
   git remote add origin https://github.com/your-username/ColorNote.git
   ```

   确保 `your-username` 和 `ColorNote` 与 `project.config.json` 中的 `github_owner` 和 `repo_name` 一致。

   > 注意：macOS/Linux 用户使用相同的命令。

5. **验证 Git 配置**：

   **Windows (PowerShell)**：

   ```powershell
   # 验证远程仓库配置
   git remote -v
   # 应该显示：origin  https://github.com/your-username/ColorNote.git (fetch)
   #          origin  https://github.com/your-username/ColorNote.git (push)
   
   # 验证当前分支
   git branch --show-current
   # 应该显示你在 project.config.json 中配置的 default_branch
   ```

   > 注意：macOS/Linux 用户使用相同的命令。

6. **确保 `project.config.json` 配置正确**：

   在继续之前，确保 `project.config.json` 中的配置与你的 Git 仓库信息一致：
   - `github_owner` 必须与你的 GitHub 用户名或组织名一致
   - `repo_name` 必须与你的仓库名称一致
   - `default_branch` 必须与你的默认分支名一致

   > **为什么需要删除 `.git/`？**
   >
   > - Preflight 校验要求 Git remote origin 必须匹配 `project.config.json` 中的仓库信息
   > - 模板仓库的 `.git/` 指向模板仓库，而不是你的项目仓库
   > - 保留模板的 Git 历史会导致 Preflight 校验失败

#### 3. 准备 Vercel 项目

- 注册/登录 Vercel 账号
- 创建或准备创建 Vercel Project
- 安装 Vercel CLI（用于本地开发）：

  ```bash
  npm i -g vercel
  ```

- 配置 Vercel Blob 存储（用于图片上传）：
  - 在 Vercel 项目设置中启用 Blob Storage
  - 获取 `BLOB_READ_WRITE_TOKEN`（可在 Vercel Dashboard 的 Environment Variables 中创建）
  - 或使用 Vercel CLI 命令：`vercel env pull` 获取环境变量

#### 4. 准备 TiDB Cloud 数据库

- 注册 TiDB Cloud 账号
- 创建数据库集群，获取连接信息：
  - Host
  - Port（默认 4000）
  - Username
  - Password
- 创建两个数据库：
  - 业务数据库（如 `colornote_db`）
  - 测试数据库（如 `colornote_test_db`，必须与业务库不同）

---

### 第二步：配置项目信息

#### 2.1 在你的项目中创建并填写 `project.config.json`

> **重要说明**：
>
> - 模板仓库中的 `project.config.json` 是**示例文件**
> - 你需要在**你自己的 ColorNote 项目**中创建该文件
> - 该文件有两个用途：
>   1. 用于替换 `spec-template.md` 中的占位符
>   2. 在 Preflight 校验中使用（Plan 章节中会读取此文件进行 Git/Vercel 相关校验）

在你的项目根目录创建 `project.config.json`，填写你的实际项目信息：

```json
{
    "github_owner": "your-github-username",
    "repo_name": "ColorNote",
    "default_branch": "main",
    "vercel_project_name": "colornote"
}
```

**重要**：这个文件是模板渲染和 Preflight 校验的单一事实来源（SSOT），所有占位符替换和校验都基于此文件。

#### 2.2 处理 `spec-template.md` 中的占位符

##### 方法一：使用自动化脚本（推荐）

使用提供的脚本自动替换占位符：

```bash
# 运行 Python 脚本（会自动检查并安装依赖）
python scripts/render-spec.py
# 或
./scripts/render-spec.py
```

脚本会自动检查并安装 Jinja2 依赖（如果未安装）。

脚本会：

- 读取 `project.config.json` 中的配置值
- 使用 Jinja2 模板引擎替换 `spec-template.md` 中的所有占位符
- 生成 `spec-template-rendered.md`（原模板文件保持不变）
- 自动验证替换是否成功，并显示替换统计

##### 方法二：手动替换

如果你想手动替换，可以在 `spec-template.md` 中，将所有占位符替换为 `project.config.json` 中的实际值：

- `{{github_owner}}` → `project.config.json` 中的 `github_owner`
- `{{repo_name}}` → `project.config.json` 中的 `repo_name`
- `{{default_branch}}` → `project.config.json` 中的 `default_branch`
- `{{vercel_project_name}}` → `project.config.json` 中的 `vercel_project_name`

你可以使用文本编辑器的查找替换功能完成替换。

#### 2.3 创建并填写 `.env` 文件

```bash
# 复制模板
cp env.example .env
```

编辑 `.env`，填写真实的数据库连接信息：

```bash
APP_ENV=local
FLASK_ENV=development

DB_HOST=your-tidb-host.tidbcloud.com
DB_PORT=4000
DB_USERNAME=your-username
DB_PASSWORD=your-password

DB_DATABASE=colornote_db
DB_TEST_DATABASE=colornote_test_db

DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_RECYCLE=300
DB_CONNECT_TIMEOUT=10

# Vercel Blob Storage
BLOB_READ_WRITE_TOKEN=your-blob-read-write-token
```

**注意**：

- `DB_DATABASE` 和 `DB_TEST_DATABASE` 必须非空且不相同
- `BLOB_READ_WRITE_TOKEN` 必须配置（用于图片上传到 Vercel Blob）
- 不要将 `.env` 文件提交到 Git（建议添加到 `.gitignore`）

---

### 第三步：在你的项目中初始化 Spec-Kit

在你的 ColorNote 项目目录中，运行以下命令初始化 Spec-Kit：

```bash
# 进入你的项目目录
cd /path/to/your/ColorNote

# 初始化 Spec-Kit
specify init .
```

在初始化过程中，你将被提示选择所使用的 AI 助手（如 Claude、Copilot、Gemini、Codebuddy 等）。

初始化完成后，Spec-Kit 会在你的项目中创建必要的配置文件和目录结构。

---

### 第四步：使用 AI 助手命令导入规范

**这是关键步骤**：`spec-template.md` 的三个章节直接对应 Spec-Kit 的三个开发阶段。使用 AI 助手的 Spec-Kit 命令，将模板中已处理好的内容复制到相应的命令中。

> **参考**：[Spec-Kit 官方文档](https://raw.githubusercontent.com/github/spec-kit/refs/heads/main/README.md) 中的三个阶段：
>
> - **Step 2**: Establish project principles → `/speckit.constitution`
> - **Step 3**: Create the spec → `/speckit.specify`
> - **Step 4**: Create a technical implementation plan → `/speckit.plan`

#### 4.1 导入 Constitution（项目宪章）

对应 Spec-Kit 的 **Step 2: Establish project principles**。

在你的 AI 助手中，使用以下命令：

```text
/speckit.constitution
```

然后将 `spec-template-rendered.md`（或已替换占位符的 `spec-template.md`）中 **Constitution 章节**的内容（从 `## Constitution` 开始，到 `---` 之前）**完整复制**粘贴到命令中。

> **提示**：如果使用了 `scripts/render-spec.py` 脚本，建议使用生成的 `spec-template-rendered.md` 文件，确保所有占位符都已替换。

**示例**：

```text
/speckit.constitution

## Constitution

**项目名称**：ColorNote - 全栈便利贴应用

**GitHub 仓库名**：`ColorNote`  
**Vercel 项目名**：`colornote`

### 项目元信息（强约束）

- GitHub repository: `your-username/ColorNote`
- Default branch: `main`
- Git remote (origin): `https://github.com/your-username/ColorNote.git`

...（继续复制完整的 Constitution 章节内容）
```

#### 4.2 导入 Specify（需求规格）

对应 Spec-Kit 的 **Step 3: Create the spec**。

在你的 AI 助手中，使用以下命令：

```text
/speckit.specify
```

然后将 `spec-template-rendered.md`（或已替换占位符的 `spec-template.md`）中 **Specify 章节**的内容（从 `## Specify` 开始，到 `---` 之前）**完整复制**粘贴到命令中。

> **注意**：Spec-Kit 的 `/speckit.specify` 命令要求关注"要做什么"和"为什么"，而不是技术栈。本模板的 Specify 章节已经按照这个原则编写。

#### 4.3 导入 Plan（实现计划）

对应 Spec-Kit 的 **Step 4: Create a technical implementation plan**。

在你的 AI 助手中，使用以下命令：

```text
/speckit.plan
```

然后将 `spec-template-rendered.md`（或已替换占位符的 `spec-template.md`）中 **Plan 章节**的内容（从 `## Plan` 开始，到文件末尾）**完整复制**粘贴到命令中。

> **注意**：Plan 章节包含技术栈和架构选择，这正是 `/speckit.plan` 命令所需要的内容。

---

### 第五步：使用 Spec-Kit 进行开发

当规范导入完成后，你可以开始使用 Spec-Kit 进行项目开发。

#### 5.1 生成开发任务

使用以下命令将实现计划分解为具体的开发任务：

```text
/speckit.tasks
```

Spec-Kit 会根据你导入的 Plan 内容，生成可执行的开发任务列表。

#### 5.2 开始实现

根据生成的任务列表，开始编写代码。你可以：

- 使用 `/speckit.constitution` 查看项目宪章
- 使用 `/speckit.specify` 查看需求规格
- 使用 `/speckit.plan` 查看实现计划
- 使用 `/speckit.tasks` 查看和管理开发任务

#### 5.3 重要提醒

在开始实现之前，务必完成 Plan 中提到的 Preflight 校验，确保：

- Git 仓库配置正确
- 环境变量配置完整（包括 `BLOB_READ_WRITE_TOKEN`）
- 数据库连接正常
- Vercel 本地环境可用
- Vercel Blob 存储已配置

---

## 📝 模板文件详细说明

### `spec-template.md` 结构

模板文件包含三个主要章节：

1. **Constitution（项目宪章）**
   - 项目元信息和强约束（Guardrail）
   - 项目描述与范围
   - 技术栈约束原则（原则性要求，非具体技术选型）
   - 质量与交付红线

2. **Specify（需求规格）**
   - 功能模块详细需求（CRUD 操作）
   - 移动端适配要求
   - 部署与环境一致性要求
   - 性能要求

3. **Plan（实现计划）**
   - 开发前置校验
   - 技术栈选型（具体技术选型）
   - 架构设计
   - 数据模型设计
   - API 设计
   - 测试方案
   - CI/CD 配置

### 占位符说明

模板中使用的占位符及其来源：

| 占位符 | 来源 | 说明 |
|--------|------|------|
| `{{github_owner}}` | `project.config.json` | GitHub 用户名或组织名 |
| `{{repo_name}}` | `project.config.json` | 仓库名称 |
| `{{default_branch}}` | `project.config.json` | 默认分支名（如 `main`） |
| `{{vercel_project_name}}` | `project.config.json` | Vercel 项目名称 |

---

## ❓ 常见问题

### Q1: 为什么需要提前准备 GitHub / Vercel / TiDB？

因为 Constitution 和 Plan 中将仓库信息、分支名、Vercel 运行方式、TiDB 环境变量校验写成了"强约束/红线"。如果不提前准备，Preflight 校验将无法通过，导致无法开始开发。

### Q2: 为什么要使用 AI 助手命令而不是直接生成文件？

Spec-Kit 的设计理念是通过 AI 助手进行交互式开发。使用 `/speckit.constitution`、`/speckit.specify`、`/speckit.plan` 等命令，可以让 AI 助手理解项目规范，并在后续开发过程中持续引用这些规范，确保实现与规范一致。

### Q3: 如何验证占位符替换是否正确？

**如果使用脚本**：

运行 `python3 scripts/render-spec.py` 后，脚本会自动验证并显示替换统计。如果看到"✓ 所有占位符已成功替换"，说明替换成功。

**如果手动替换**：

检查 `spec-template.md` 或 `spec-template-rendered.md` 中：

- 不再包含任何 `{{...}}` 格式的占位符
- 所有 GitHub 仓库 URL 指向正确的仓库
- 所有分支名与实际仓库分支一致
- Vercel 项目名与实际项目一致

### Q4: `project.config.json` 应该放在哪里？

`project.config.json` 应该放在**你自己的 ColorNote 项目**的根目录中，而不是模板仓库中。

- **模板仓库中的 `project.config.json`**：只是示例文件，用于参考格式
- **你项目中的 `project.config.json`**：实际使用的配置文件，用于：
  - 替换 `spec-template.md` 中的占位符
  - Preflight 校验时读取（Plan 章节中会使用此文件进行 Git/Vercel 相关校验）

### Q5: 如果修改了 `project.config.json`，需要重新导入吗？

是的。如果修改了你项目中的 `project.config.json`，需要：

1. 重新运行 `python3 scripts/render-spec.py` 生成新的 `spec-template-rendered.md`（或手动替换 `spec-template.md` 中的占位符）
2. 重新使用 AI 助手命令导入更新后的规范内容
3. 确保 Preflight 校验能够读取到更新后的配置

### Q6: `.env` 文件应该提交到 Git 吗？

**不应该**。`.env` 包含敏感信息（数据库密码等），应该添加到 `.gitignore` 中。只提交 `env.example` 作为模板。

### Q7: 这个仓库是实际项目还是模板？

这是一个**示例模板仓库**（`Spec-Kit-Example-ColorNote`），用于学习和演示 Spec-Kit 的使用方法。你需要：

1. Fork 或 Clone 本仓库，获取模板文件
2. **删除 `.git/` 目录**（重要：这是模板仓库的 Git 历史）
3. 创建你自己的 ColorNote 项目仓库
4. 重新初始化 Git，连接到你的项目仓库
5. 在你的项目中创建 `project.config.json` 和 `.env` 文件（参考模板中的示例）
6. 在你的项目中初始化 Spec-Kit：`specify init .`
7. 使用 AI 助手命令，将模板内容导入到 Spec-Kit
8. 开始实际的项目开发

本仓库本身不包含实际运行的项目代码，只包含模板文件和配置示例。

### Q8: 支持哪些 AI 助手？

Spec-Kit 支持多种 AI 助手，包括但不限于：

- Claude（Anthropic）
- GitHub Copilot
- Gemini（Google）
- Codebuddy CLI

在运行 `specify init .` 时，你可以选择使用的 AI 助手。

### Q9: 为什么需要删除 `.git/` 目录？

**必须删除的原因**：

1. **Preflight 校验要求**：Plan 章节中的 Preflight 校验会检查 Git remote origin 是否匹配 `project.config.json` 中的仓库信息。如果保留模板仓库的 `.git/`，origin 会指向模板仓库（`thiswind/Spec-Kit-Example-ColorNote`），而不是你的项目仓库，导致 Preflight 校验失败。

2. **避免混淆**：模板仓库的 Git 历史与你自己的项目无关，保留会导致：
   - Git 历史混乱（包含模板仓库的提交记录）
   - 无法正确推送到你自己的仓库
   - Preflight 校验无法通过

3. **正确的流程**：

   **Windows (PowerShell)**：

   ```powershell
   # 1. 克隆模板
   git clone https://github.com/thiswind/Spec-Kit-Example-ColorNote.git
   cd Spec-Kit-Example-ColorNote
   
   # 2. 删除模板的 Git 历史
   Remove-Item -Recurse -Force .git
   
   # 3. 重新初始化 Git，连接到你的仓库
   git init
   git remote add origin https://github.com/your-username/ColorNote.git
   git branch -M main
   
   # 4. 填写 project.config.json（确保 github_owner 和 repo_name 匹配你的仓库）
   # 5. 继续后续步骤...
   ```

   > **macOS / Linux (Bash / Zsh) 用户**：将第 2 步的 `Remove-Item -Recurse -Force .git` 替换为 `rm -rf .git`，其他命令相同。

4. **验证**：重新初始化后，运行 `git remote -v` 应该显示你的仓库地址，而不是模板仓库地址。

---

## 🔗 相关资源

- [Spec-Kit 官方仓库](https://github.com/github/spec-kit)
- [Spec-Kit 文档](https://github.github.com/spec-kit/)
- [Vercel CLI 文档](https://vercel.com/docs/cli)
- [Vercel Blob 文档](https://vercel.com/docs/storage/vercel-blob)
- [TiDB Cloud 文档](https://docs.pingcap.com/tidbcloud/)
- [Flask 文档](https://flask.palletsprojects.com/)

---

## 📄 许可证

本项目模板文件遵循相应的开源许可证。使用本模板时，请遵守相关许可证要求。
