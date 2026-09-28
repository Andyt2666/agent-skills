---
name: "meta-skill-collection-builder"
description: "从公开仓库批量克隆 skill 并本地化，构建自己的 skill 合集包。涵盖许可分诊（哪些能克隆、哪些只能重写）、frontmatter 批量改写、中文触发词注入、YAML 校验、以及踩坑清单。触发词：建 skill 合集、克隆 skill、批量移植 skill、技能合集、skill collection、本地化 skill、awesome skills、微调 skill、上游仓库。"
license: "本地原创"
---

# Skill 合集构建器

## 📖 说明

把「从上游仓库批量拉 skill → 本地化微调 → 校验 → 成包」这套流程固化下来。
本文来自一次真实的 39 个 skill 合集构建实践，含实际踩到的坑。

## 一、第一步永远是：许可分诊

**不先看许可就动手 = 埋雷。** 把上游每个 skill 分成三堆：

| 堆 | 判据 | 处理方式 |
|---|---|---|
| 🟢 **可克隆** | 目录内有 `LICENSE` / `LICENSE.txt`，且是 MIT / Apache-2.0 / BSD 等 | 整目录复制，保留许可文件，加本地化层 |
| 🟡 **只能重写** | `license: Proprietary` / source-available / 无任何许可文件 | **不复制任何文本**，只借鉴思路自己写 |
| 🔴 **不可碰** | 明确禁止再分发 | 不纳入 |

**关键教训：**

- 仓库根 README 说「大部分是 Apache-2.0」**不等于**每个子目录都是。
  必须**逐个 skill 检查目录内有没有 `LICENSE.txt`**。
- **没有许可文件 ≠ 可以随便用**。默认按「保留所有权利」处理，
  归到 🟡 重写堆。
- 有些仓库会在 README 里单独点名哪几个子目录是 source-available
  （例如 Anthropic 的 `docx/pdf/pptx/xlsx`），**这几条要照做**。

### 探测命令

```bash
for s in */; do
  for f in LICENSE LICENSE.txt LICENSE.md COPYING; do
    [ -f "$s/$f" ] && { echo "$s -> $f: $(head -2 "$s/$f" | tail -1)"; break; }
  done
done
```

## 二、拉取上游

用 codeload 拉 tarball，比 `git clone` 快且不带走 `.git`：

```bash
curl -sL "https://codeload.github.com/<owner>/<repo>/tar.gz/refs/heads/main" -o repo.tar.gz
mkdir repo && tar xzf repo.tar.gz -C repo --strip-components=1
```

先列目录再决定拉哪些：

```bash
curl -s "https://api.github.com/repos/<owner>/<repo>/contents/<path>" \
  | python -c "import sys,json;[print(x['name']) for x in json.load(sys.stdin)]"
```

## 三、本地化微调（四件事）

对每个要克隆的 skill：

1. **复制整个目录**——保留脚本、参考文件、`LICENSE.txt`，
   别只拿 `SKILL.md`（会丢依赖）
2. **改写 `name`** 为本地命名（建议 `<类别前缀>-<语义名>`，便于排序）
3. **在 `description` 末尾追加中文触发词**——这是让中文提问能命中
   该 skill 的关键，也是最有价值的一步微调
4. **在正文第一个 H1 之后插入「中文导读」区块**——一句话 / 何时触发 /
   来源与许可。**原版正文一字不改**，保证可追溯

### 命名前缀建议

| 前缀 | 类别 |
|---|---|
| `meta-` | 元技能（造 skill 的 skill） |
| `doc-` | 文档处理 |
| `design-` | 设计创意 |
| `dev-` | 开发与工程方法论 |
| `research-` | 科研学术 |
| `writing-` | 写作沟通 |
| `thinking-` | 思辨判断 |

## 四、⚠️ 最大的坑：YAML 块标量

**这个坑一定会遇到，必须处理。**

很多上游 skill 的 `description` 用的是 **YAML 块标量**：

```yaml
description: |-
  第一行
  第二行，缩进两格
  TRIGGER — ...
```

如果你只按行做正则替换（比如「找到 `description:` 那行，替换成加引号的
单行」），**续行会变成孤儿**，frontmatter 直接解析失败。

**正确做法**——先把块标量折叠成单行，再改写：

```python
import re, yaml

m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
fm_text = m.group(1)

# 方案 A：直接让 yaml 解析（最稳）
data = yaml.safe_load(fm_text)          # 块标量自动折叠成字符串
desc = " ".join(str(data["description"]).split())

# 方案 B：手工处理时，必须吃掉所有缩进续行
```

**判断有没有中招**：改写完跑一次 `yaml.safe_load`，
报 `while parsing a block mapping` 就是它。

### 另一种残留

反复替换可能留下 `description: '|- '` 这类前缀。
**别用多层正则去剥**，用锚点法最省事：

```python
i = desc.find("Reference for the Claude API")   # 找一个正文里的稳定锚点
desc = desc[i:]
```

## 五、校验（必做）

```python
import os, re, yaml
bad = []
for name in sorted(os.listdir("skills")):
    t = open(f"skills/{name}/SKILL.md", encoding="utf-8").read()
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", t, re.S)
    if not m: bad.append((name, "frontmatter 未闭合")); continue
    try:
        data = yaml.safe_load(m.group(1))
    except Exception as e:
        bad.append((name, f"YAML: {e}")); continue
    if data.get("name") != name: bad.append((name, "name 与目录名不符")); continue
    if not str(data.get("description") or "").strip():
        bad.append((name, "description 空"))
    if len(t[m.end():].strip()) < 200:
        bad.append((name, "正文过短"))
print("异常:", bad or "无")
```

**五项必查**：

1. `name` 字段 == 目录名
2. `description` 非空、且含触发词
3. YAML 能解析
4. 正文长度合理（没被截断）
5. 有 H1 标题

## 六、交付结构

```
<合集根>/
├── README.md          # 总索引：分类表 + 用途 + 触发方式 + 安装方法 + 已知边界
├── LICENSE-NOTES.md   # 逐条来源与许可 + 对外发布红线
├── tools/             # 构建与校验脚本（可复现）
│   ├── build_clones.py
│   └── validate_skills.py
└── skills/            # 平铺，可直接整体拷贝到 skills 目录
    ├── meta-*/
    ├── doc-*/
    └── ...
```

**为什么平铺**：skill 发现机制通常不递归多层子目录。
想分类就靠**命名前缀**，不要靠目录层级。

## 七、诚实性要求

- **许可状态如实标注**，不许含糊。🟡 重写堆必须在 `LICENSE-NOTES.md`
  里说明「本文件为原创重写，未复制上游文本」。
- **上游拉取日期要记**——上游会变，不记日期就无法追溯你克隆的是哪一版。
- **改了哪里要说清**。本流程只增补不改原版正文，这一点要写进 README。
- **别声称「全部微调好了」**。克隆来的 skill 内部脚本可能仍依赖原平台的
  命令与路径，这些**没适配**就要明说。
