# 第三方内容声明

本仓库的原创部分适用根目录 [`LICENSE`](./LICENSE)（MIT）。
以下内容来自第三方，**不适用** MIT 许可，各自保留原许可。

---

## 1. `anthropics/skills` — Apache License 2.0

- **来源**：<https://github.com/anthropics/skills>
- **分支 / 拉取日期**：`main` / 2026-09-23
- **许可**：Apache License 2.0
- **版权**：Copyright Anthropic PBC
- **许可全文**：各 skill 目录内的 `LICENSE.txt`

**受此许可约束的目录（14 个）：**

```
meta-skill-creator          design-frontend
design-canvas               design-theme-factory
design-brand-guidelines     design-algorithmic-art
dev-webapp-testing          dev-web-artifacts-builder
dev-mcp-builder             dev-claude-api
writing-internal-comms      writing-academy-guide
thinking-discernment        design-slack-gif
```

**本项目所做的改动**：仅改写 frontmatter 的 `name` 字段、在 `description`
末尾追加中文触发词、在正文首个 H1 之后插入中文导读区块。
**原版正文内容未作改动。** 各目录内的 `LICENSE.txt` 原样保留。

---

## 2. `obra/superpowers` — MIT License

- **来源**：<https://github.com/obra/superpowers>
- **分支 / 拉取日期**：`main` / 2026-09-23
- **许可**：MIT License
- **版权**：Copyright (c) 2025 Jesse Vincent
- **许可全文**：各 skill 目录内的 `LICENSE.txt`

**受此许可约束的目录（15 个）：**

```
meta-using-skills           meta-writing-skills
dev-brainstorming           dev-writing-plans
dev-executing-plans         dev-systematic-debugging
dev-tdd                     dev-verification
dev-requesting-review       dev-receiving-review
dev-subagent-driven         dev-dispatching-parallel
dev-git-worktrees           dev-finishing-branch
dev-diagnosing
```

> 上游的 MIT 许可文本位于仓库根目录，不在单个 skill 目录内。
> 为满足 MIT「再分发时须保留版权声明与许可文本」的要求，
> 本项目已将 MIT 许可全文**逐字复制**到上述每个 skill 目录的
> `LICENSE.txt`。

**本项目所做的改动**：同第 1 节——仅改 `name`、加中文触发词、加中文导读，
正文未改动。

---

## 3. 未纳入本仓库的第三方内容

以下技能属于 Anthropic 的 **source-available** 内容（不可再分发），
**未复制任何原始文本进本仓库**：

| 上游路径 | 上游许可状态 |
|---|---|
| `anthropics/skills` → `skills/pdf` | Proprietary / source-available |
| `anthropics/skills` → `skills/docx` | Proprietary / source-available |
| `anthropics/skills` → `skills/pptx` | Proprietary / source-available |
| `anthropics/skills` → `skills/xlsx` | Proprietary / source-available |
| `anthropics/skills` → `skills/doc-coauthoring` | 未附任何许可文件 |

本仓库中对应的 `doc-pdf`、`doc-docx`、`doc-pptx`、`doc-xlsx`、
`writing-doc-coauthoring` 五个 skill 是**完全原创的重写作品**，
只借鉴了上述技能的任务分层思路，正文、代码示例与检查清单均为本项目自撰。

---

## 4. 字体与其他资源

`design-canvas` 目录下的字体文件（`canvas-fonts/`）随上游 Apache-2.0
内容一同分发。若需单独使用这些字体，请自行核对字体本身的授权条款。

---

## 5. 汇总

| 类别 | 数量 | 许可 | 可否再分发 |
|---|---|---|---|
| 本项目原创 / 重写 | 11 | MIT | ✅ |
| `anthropics/skills` 克隆 | 14 | Apache-2.0 | ✅ 需保留 LICENSE.txt |
| `obra/superpowers` 克隆 | 15 | MIT | ✅ 需保留 LICENSE.txt |
| **合计** | **40** | — | — |
