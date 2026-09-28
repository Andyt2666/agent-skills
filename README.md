# Skill 合集包

> 个人 agent skill 合集。**40 个**技能，按「克隆开源 + 重写受限 + 原创定制」三种方式产出。
> 建立日期：2026-09-23

## 一、这是什么

一个可直接使用的 skill 合集，覆盖元技能、文档处理、设计创意、软件开发、
科研学术、写作沟通六大方向。每个 skill 都是独立目录，含一份 `SKILL.md`。

**三条产出路线：**

| 路线 | 数量 | 做法 | 许可状态 |
|---|---|---|---|
| 🔵 **克隆** | 29 | 整目录复制开源 skill，加中文导读 + 中文触发词 | Apache-2.0 / MIT，可自由分发 |
| 🟡 **重写** | 5 | 只借鉴工作流思路，`SKILL.md` 完全自己写 | 原版 source-available，本包内为**原创** |
| 🟢 **原创** | 6 | 科研工作流定制 + 合集构建方法论，无外部来源 | 完全自有 |

## 二、目录结构

```
<repo-root>\
├── README.md                 ← 本文件（总索引）
├── LICENSE                   ← MIT，覆盖本仓库原创部分
├── LICENSE-NOTES.md          ← 许可分诊结论与对外发布红线
├── THIRD-PARTY-NOTICES.md    ← 第三方内容逐条声明（Apache-2.0 / MIT）
├── .gitattributes            ← 锁定 LF，保护克隆内容与 .sh 可执行性
├── .gitignore
├── tools\                    ← 构建 / 校验 / 部署脚本（可复现）
│   ├── build_clones.py       ← 批量克隆 + 本地化微调
│   ├── validate_skills.py    ← 合集完整性校验
│   └── install_skills.py     ← 挂载 / 卸载到 skills 目录（默认 dry-run）
└── skills\                   ← 40 个 skill（可直接整体拷贝使用）
    ├── meta-*                ← 元技能（4）
    ├── doc-*                 ← 文档处理（4）
    ├── design-*              ← 设计创意（6）
    ├── dev-*                 ← 软件开发与工程方法论（17）
    ├── research-*            ← 科研学术（5）
    ├── writing-*             ← 写作沟通（3）
    └── thinking-*            ← 思辨（1）
```

**许可文件分布**：40 个 skill 目录中，**29 个带 `LICENSE.txt`**
（14 个 Apache-2.0 + 15 个 MIT）。剩余 11 个是本仓库原创 / 重写作品，
适用根目录的 MIT 许可。

## 三、技能清单

### 🧩 元技能 meta-（4）

| Skill | 一句话 | 来源 |
|---|---|---|
| `meta-skill-creator` | 从零创建、迭代改进、跑评测优化 skill | 🔵 anthropics/skills |
| `meta-skill-collection-builder` | 从上游仓库批量克隆 skill 建自己的合集 | 🟢 原创 |
| `meta-writing-skills` | 把可复用工作流沉淀成 skill | 🔵 obra/superpowers |
| `meta-using-skills` | skill 体系入口：先判断该调哪个 | 🔵 obra/superpowers |

### 📄 文档处理 doc-（4）

| Skill | 一句话 | 来源 |
|---|---|---|
| `doc-pdf` | PDF 读写拆合、表单、OCR、生成 | 🟡 重写 |
| `doc-docx` | Word 创建/编辑/修订/批注 | 🟡 重写 |
| `doc-pptx` | PPT 生成/套模板/改页/备注 | 🟡 重写 |
| `doc-xlsx` | 表格创建/公式/清洗/图表 | 🟡 重写 |

### 🎨 设计创意 design-（6）

| Skill | 一句话 | 来源 |
|---|---|---|
| `design-frontend` | UI 视觉方向，避开模板感 | 🔵 anthropics/skills |
| `design-canvas` | 海报级平面设计 | 🔵 anthropics/skills |
| `design-theme-factory` | 成批生成协调配色/字体主题 | 🔵 anthropics/skills |
| `design-brand-guidelines` | 品牌规范落地 | 🔵 anthropics/skills |
| `design-algorithmic-art` | 生成式/参数化艺术 | 🔵 anthropics/skills |
| `design-slack-gif` | 聊天 GIF 动图 | 🔵 anthropics/skills |

### 💻 软件开发 dev-（17）

**工具类（4）**

| Skill | 一句话 | 来源 |
|---|---|---|
| `dev-webapp-testing` | 浏览器自动化测 Web 应用 | 🔵 anthropics/skills |
| `dev-web-artifacts-builder` | 可交互单文件网页产物 | 🔵 anthropics/skills |
| `dev-mcp-builder` | 从零写 MCP server | 🔵 anthropics/skills |
| `dev-claude-api` | Anthropic API 用法速查 | 🔵 anthropics/skills |

**方法论类（13，全部来自 obra/superpowers）**

| Skill | 一句话 |
|---|---|
| `dev-brainstorming` | 动手前把意图/需求/设计聊透 |
| `dev-writing-plans` | 把设计落成可验证的分步计划 |
| `dev-executing-plans` | 按计划执行并逐项验证 |
| `dev-systematic-debugging` | 系统化排障：复现 → 定位 → 修复 |
| `dev-tdd` | 红-绿-重构 |
| `dev-verification` | 声称「做完了」前必须拿出证据 |
| `dev-requesting-review` | 发起代码评审 |
| `dev-receiving-review` | 处理评审意见 |
| `dev-subagent-driven` | 子代理驱动开发 |
| `dev-dispatching-parallel` | 并行派发独立任务 |
| `dev-git-worktrees` | git worktree 隔离并行分支 |
| `dev-finishing-branch` | 开发分支收尾合并 |
| `dev-diagnosing` | 排查 skill 体系自身问题 |

### 🔬 科研学术 research-（5，全部原创）

| Skill | 一句话 |
|---|---|
| `research-paper-reading` | 四遍读法 + 结构化笔记 + 参数来源分级 |
| `research-lit-review` | 检索 → 筛选 → 归类 → 找缺口 |
| `research-experiment-log` | 实验记录 + **三级来源标注** + 缺口台账 |
| `research-figure-spec` | 期刊投稿图规范：矢量、配色、误差棒 |
| `research-formula-typesetting` | LaTeX 公式、符号表、单位与量纲 |

### ✍️ 写作沟通 writing-（3）

| Skill | 一句话 | 来源 |
|---|---|---|
| `writing-doc-coauthoring` | 文档共创三阶段工作流 | 🟡 重写 |
| `writing-internal-comms` | 周报/公告/复盘 | 🔵 anthropics/skills |
| `writing-academy-guide` | 教程与课程材料 | 🔵 anthropics/skills |

### 🧠 思辨 thinking-（1）

| Skill | 一句话 | 来源 |
|---|---|---|
| `thinking-discernment` | 信息不足/带预设时先辨别再回答 | 🔵 anthropics/skills |

## 四、怎么安装使用

### 方式一：用脚本挂载（推荐）

```bash
# 先看会做什么（默认 dry-run，不动任何文件）
python tools/install_skills.py --all

# 确认后真正执行
python tools/install_skills.py --all --yes

# 只挂需要的几个
python tools/install_skills.py --only research-paper-reading,research-experiment-log --yes

# 卸载（只删本合集装进去的，不动你原有的 skill）
python tools/install_skills.py --uninstall --all --yes
```

脚本默认目标是 `~/.workbuddy-ai/skills`（通常已 junction 到
实际的技能目录）。**已存在的同名 skill 默认跳过**，
加 `--force` 才覆盖——不会误伤你原有的东西。

### 方式二：手动拷贝

```bash
cp -r skills/* ~/.workbuddy-ai/skills/
```

### 方式三：留在原地

直接在本仓库里用，不必搬走。

> ⚠️ **别一次全挂**。40 个 skill 会让技能列表变长，
> 可能拉低触发准确率。建议先挂真正用得上的那几类。

## 五、工具脚本

`tools/` 下三个脚本，让这套合集**可复现、可维护、可部署**：

| 脚本 | 作用 |
|---|---|
| `validate_skills.py` | 校验合集完整性（YAML 合法性、name 一致性、触发词、正文完整性） |
| `install_skills.py` | 挂载 / 卸载到 skills 目录，默认 dry-run |
| `build_clones.py` | 从上游重建克隆部分，含 MIT 许可自动补入 |

```bash
# 改过任何 SKILL.md 之后，跑一次校验
python tools/validate_skills.py skills
```

**它能抓出的典型问题**：YAML 块标量改写事故、`name` 与目录名不一致、
`description` 缺触发词、正文被截断。

## 六、几个使用要点

1. **中文触发词已注入 description**——克隆类 skill 的 description 末尾
   都追加了「中文触发词：…」，中文提问也能命中。
2. **每个 SKILL.md 开头有「📖 中文导读」**——说明这个 skill 干什么、
   何时触发、来源与许可，原版正文保持未改动。
3. **内置技能优先**——文档类若本机已有 `tencent-docx` / `tencent-pptx` /
   `tencent-docs-sheetagent` / `pdf` / `pdfkit-py`，优先复用；
   本合集的 `doc-*` 负责**选路与质检**。
4. **科研类面向实验与仿真场景定制**——`research-experiment-log` 强制三级来源标注
   （实测/论文值/理论假设），与项目铁律一致。

## 七、已知边界

- **`design-canvas`（5.6M）和 `dev-claude-api`（1.4M）体积较大**，
  因为原版带了完整的参考文件与示例资源。不需要可单独删。
- **`doc-pdf` 的中文 OCR** 依赖本机 Tesseract 的 `chi_sim` 语言包，
  没装就做不了，skill 里已注明。
- **`design-slack-gif`** 生成的 GIF 用于聊天场景，
  本环境对 GIF 制作的支持有限，必要时手动处理。
- 克隆类 skill 的**内部脚本仍按原仓库路径习惯写**（如 `claude` 命令），
  在非 Claude Code 环境下部分脚本需自行适配。**这部分没做适配。**
- **行尾已锁 LF**（见 `.gitattributes`）。如果你用别的编辑器打开
  克隆来的文件，注意别让它把 LF 改成 CRLF——5 个 `.sh` 脚本会因此失效。
- 本仓库**尚未推送到远程**。许可文件已按对外发布标准备齐，但推送前
  建议先确认根 `LICENSE` 的许可选择（当前是 MIT）。

## 八、后续可做

- [x] 建 git 仓库（已完成，本地 `main` 分支，首次提交 339 文件）
- [x] 补齐第三方许可文件（superpowers 的 MIT 文本已逐字复制到 15 个目录）
- [x] **推送到 GitHub**（已完成，public）
- [ ] 挑几个高频的，按你自己的实际用法继续「微调」（改流程、删冗余步骤）
- [ ] 把 `research-*` 五个与实际仿真工作台打通
- [ ] 清理：删掉用不上的，避免技能列表过长影响触发准确率

---

许可与来源明细见 [`LICENSE-NOTES.md`](./LICENSE-NOTES.md)。
