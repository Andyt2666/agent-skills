# 来源与许可明细

本合集包共 40 个 skill，按许可状态分三类。**对外发布前请先读第三节的红线提示。**

## 一、🔵 克隆类（29 个）—— 可自由分发

整目录复制自公开仓库，保留原始文件与 `LICENSE`，仅增补中文导读与中文触发词。

### 来源 A：`anthropics/skills`（Apache-2.0，14 个）

| 本包名称 | 原路径 | 原许可 |
|---|---|---|
| `meta-skill-creator` | `skills/skill-creator` | Apache-2.0 |
| `design-frontend` | `skills/frontend-design` | Apache-2.0 |
| `design-canvas` | `skills/canvas-design` | Apache-2.0 |
| `design-theme-factory` | `skills/theme-factory` | Apache-2.0 |
| `design-brand-guidelines` | `skills/brand-guidelines` | Apache-2.0 |
| `design-algorithmic-art` | `skills/algorithmic-art` | Apache-2.0 |
| `dev-webapp-testing` | `skills/webapp-testing` | Apache-2.0 |
| `dev-web-artifacts-builder` | `skills/web-artifacts-builder` | Apache-2.0 |
| `dev-mcp-builder` | `skills/mcp-builder` | Apache-2.0 |
| `dev-claude-api` | `skills/claude-api` | Apache-2.0 |
| `writing-internal-comms` | `skills/internal-comms` | Apache-2.0 |
| `writing-academy-guide` | `skills/academy-guide` | Apache-2.0 |
| `thinking-discernment` | `skills/discernment-nudge` | Apache-2.0 |
| `design-slack-gif` | `skills/slack-gif-creator` | Apache-2.0 |

来源：<https://github.com/anthropics/skills> ｜ 拉取分支：`main` ｜ 拉取日期：2026-09-23

各 skill 目录内保留原始 `LICENSE.txt`（Apache License 2.0）。
按 Apache-2.0 条款：**保留版权声明与许可文本**即可自由使用、修改、再分发。

### 来源 B：`obra/superpowers`（MIT，15 个）

| 本包名称 | 原路径 |
|---|---|
| `meta-using-skills` | `skills/using-superpowers` |
| `meta-writing-skills` | `skills/writing-skills` |
| `dev-brainstorming` | `skills/brainstorming` |
| `dev-writing-plans` | `skills/writing-plans` |
| `dev-executing-plans` | `skills/executing-plans` |
| `dev-systematic-debugging` | `skills/systematic-debugging` |
| `dev-tdd` | `skills/test-driven-development` |
| `dev-verification` | `skills/verification-before-completion` |
| `dev-requesting-review` | `skills/requesting-code-review` |
| `dev-receiving-review` | `skills/receiving-code-review` |
| `dev-subagent-driven` | `skills/subagent-driven-development` |
| `dev-dispatching-parallel` | `skills/dispatching-parallel-agents` |
| `dev-git-worktrees` | `skills/using-git-worktrees` |
| `dev-finishing-branch` | `skills/finishing-a-development-branch` |
| `dev-diagnosing` | `skills/diagnosing-superpowers` |

来源：<https://github.com/obra/superpowers> ｜ 拉取分支：`main` ｜ 拉取日期：2026-09-23
版权：Copyright (c) 2025 Jesse Vincent ｜ 许可：MIT

**MIT 要求**：再分发时须保留版权声明与许可文本。
上游的 MIT 文本位于仓库根目录，**不在单个 skill 目录里**，
所以只拷 `SKILL.md` 会丢掉署名。

> ✅ **已处理**（2026-09-28）：MIT 许可全文已**逐字复制**到上述 15 个
> skill 目录的 `LICENSE.txt`，并在 `tools/build_clones.py` 里固化了这一步，
> 下次重建会自动补入。目前 40 个 skill 目录中 29 个带 `LICENSE.txt`。

## 二、🟡 重写类（5 个）—— 本包内为原创作品

以下 5 个 skill 的**源技能**属 Anthropic 的 source-available 内容
（其 `SKILL.md` 中标注 `license: Proprietary` 或未附许可文件），
**不可再分发**。因此这里**没有复制任何原始文本**，只借鉴了其任务分层思路，
正文、代码示例、检查清单均为本地原创。

| 本包名称 | 借鉴的源技能 | 源技能许可状态 | 本文件实际状态 |
|---|---|---|---|
| `doc-pdf` | `anthropics/skills` → `skills/pdf` | Proprietary（source-available） | 原创重写 |
| `doc-docx` | `anthropics/skills` → `skills/docx` | Proprietary（source-available） | 原创重写 |
| `doc-pptx` | `anthropics/skills` → `skills/pptx` | Proprietary（source-available） | 原创重写 |
| `doc-xlsx` | `anthropics/skills` → `skills/xlsx` | Proprietary（source-available） | 原创重写 |
| `writing-doc-coauthoring` | `anthropics/skills` → `skills/doc-coauthoring` | **无许可文件**（按不可再分发处理） | 原创重写 |

**为什么 `doc-coauthoring` 也归到这一类**：该技能目录下**没有任何 LICENSE 文件**，
仓库 README 也未将其列入 Apache-2.0 范围。按最保守原则处理——
只借鉴其「三阶段工作流」的思想，不复制文本。

## 三、🟢 原创类（5 个）—— 完全自有

无外部来源，面向实验与仿真科研场景
定制，含项目特有的科学诚实要求（三级参数来源标注）。

| 本包名称 | 说明 |
|---|---|
| `research-paper-reading` | 论文四遍读法 + 参数来源分级 |
| `research-lit-review` | 文献调研四步法 + 检索可复现记录 |
| `research-experiment-log` | 实验记录规范 + 三级来源标注 + 缺口台账 |
| `research-figure-spec` | 期刊投稿图规范 |
| `research-formula-typesetting` | LaTeX 公式与符号一致性 |

---

## ⚠️ 四、对外发布前的红线提示

**如果打算把本合集推到 GitHub 或对外分享：**

1. **可以带**：29 个克隆类（Apache-2.0 / MIT）+ 5 个重写类 + 6 个原创类。
2. **必须做**（**均已完成**）：
   - ✅ 仓库根 `LICENSE` 已放（MIT，覆盖原创部分）
   - ✅ 各克隆 skill 内的 `LICENSE.txt` 已保留（29 个）
   - ✅ `THIRD-PARTY-NOTICES.md` 已列明两个上游仓库的出处与版权
   - ✅ `obra/superpowers` 的 MIT 文本已注明版权归 Jesse Vincent
3. **不要做**：
   - ❌ 不要从上游仓库另行复制 `pdf` / `docx` / `pptx` / `xlsx` /
     `doc-coauthoring` 的原始文件进本合集——那是 source-available，
     再分发有风险。
   - ❌ 不要删除各克隆 skill 里的 `LICENSE.txt`。
4. **本地自用不受限制**：以上红线只针对对外发布。自己用随便。

## 五、拉取记录

| 项 | 值 |
|---|---|
| 拉取日期 | 2026-09-23 |
| `anthropics/skills` | `main` 分支 tarball，约 3.7 MB |
| `obra/superpowers` | `main` 分支 tarball，约 640 KB |
| 微调方式 | 改写 `name`、在 `description` 末尾追加中文触发词、在正文 H1 后插入中文导读区块；**原版正文内容未改动** |
