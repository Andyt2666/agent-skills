---
name: "doc-docx"
description: "Word 文档（.docx/.dotx）的创建、读取、编辑与分析。涵盖报告/备忘录/信件/模板生成、目录与页码、页眉页脚、图片插入替换、查找替换、修订痕迹（tracked changes）、批注、以及把既有内容整理成规范 Word 文档。触发词：Word、docx、word 文档、报告、备忘录、信件、模板、目录、页码、修订、批注、红头文件。"
license: "本地原创，借鉴 anthropics/skills 的 docx 技能工作流（该技能为 source-available，本文件未复制其文本）"
---

# Word 文档处理

## 📖 说明

**独立重写版**。Anthropic 官方 `docx` 技能是 source-available 许可、不可再分发，
这里不克隆原文件，只借鉴其「按任务选路径」的分层思路，正文与代码全部原创。

## 零、核心认知：.docx 就是一个 ZIP

先记住这一条，后面所有操作都顺了：

```
report.docx  ──unzip──▶  word/document.xml      （正文）
                         word/styles.xml        （样式定义）
                         word/numbering.xml     （编号/列表）
                         word/media/*           （图片）
                         word/comments.xml      （批注）
                         [Content_Types].xml    （类型声明）
```

**因此有两条完全不同的路：**

| 任务 | 走哪条路 |
|---|---|
| 从零生成 | 用库（`python-docx` / docx-js）**写** XML |
| 改既有文档 | 解包 → **直接改** `document.xml` → 重新打包 |
| 只读内容 | 用库直接读，或解包读 XML |

**改既有文档时优先解包改 XML**，因为库会丢掉它不认识的结构
（复杂页眉、内容控件、域代码），改完文档就坏了。

## 一、环境

```bash
python -m venv .venv && .venv/Scripts/pip install python-docx lxml
```

Node 侧（生成用）：

```bash
npm i docx        # 生成
npm i -g docx-cli # 可选
```

**若本机已有 `tencent-docx` 内置技能，优先复用**——本 skill 负责选路与质检。

## 二、从零生成

### python-docx

```python
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
doc.add_heading("报告标题", level=1)

p = doc.add_paragraph("正文段落。")
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.first_line_indent = Pt(21)   # 首行缩进 2 字符

doc.add_page_break()
doc.save("out.docx")
```

**中文字体必须同时设 `eastAsia`**，只设 `font.name` 中文仍是默认宋体：

```python
from docx.oxml.ns import qn
run = p.add_run("中文内容")
run.font.name = "Times New Roman"
run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
```

### 目录与页码

- **目录**：python-docx **不支持**生成目录域。做法是插入 `TOC` 域，
  打开文档后按 F9 更新；或改用模板。
  **不要假装目录已经生成好了**——它需要用户更新一次域。
- **页码**：需改 `sectPr` 里的 `footerReference`，比想象中麻烦。
  建议直接用一个带页码的模板文档做基底。

## 三、改既有文档（解包法）

```bash
unzip -o report.docx -d unpacked
# 编辑 unpacked/word/document.xml
cd unpacked && zip -r ../report_new.docx . -x '.*'
```

**三条铁律：**

1. **不要格式化 XML**——不要 pretty-print。Word 对空白敏感，
   重排缩进可能改变文本内容或破坏结构。
2. **用 lxml 做替换，不要正则**——正则处理 XML 迟早出事。
3. **改完必须打开验证**——解包重打包后 Word 报「文档已损坏」是高频事故。

### 查找替换

```python
from lxml import etree
tree = etree.parse("unpacked/word/document.xml")
for t in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
    if t.text and "旧词" in t.text:
        t.text = t.text.replace("旧词", "新词")
tree.write("unpacked/word/document.xml", xml_declaration=True,
           encoding="UTF-8", standalone=True)
```

**注意**：Word 会把一个词拆进多个 `<w:t>`（因为拼写/格式标记），
简单字符串替换可能漏掉。要可靠替换，先检查相邻 run 是否被拆开。

## 四、修订痕迹与批注

- **修订（tracked changes）**：需要在 XML 里写 `<w:ins>` / `<w:del>` 包裹节点，
  并带 `w:author` / `w:date`。手写容易漏，建议用现成库或脚本工具。
- **批注**：写 `word/comments.xml` + 正文里插 `commentRangeStart/End` 引用。
- **红线稿**：改完用 `--author "<署名>"` 之类的参数自检，确认每条改动都被标记。
  署名统一用你的 GitHub ID 或真实姓名。

## 五、质检清单

1. **能打开**——Word / WPS 打开不报「需要修复」
2. **中文没变字体**——`eastAsia` 设了没
3. **页码/目录**——域是否需要用户更新，要提前说明
4. **图片没丢**——`word/media/` 数量与预期一致
5. **修订标记完整**——红线稿逐条可查

## 六、诚实性要求

- 目录、页码这类**依赖域更新的功能**，交付时必须明说「需按 F9 更新」，
  不能装作已就绪。
- 解包改 XML 有**损坏风险**，改前先备份原件（`cp report.docx report.docx.bak`）。
- 复杂模板（多节、奇偶页不同页眉）不要承诺「完美还原」——
  先说明能力边界。
