---
name: "doc-pptx"
description: "PowerPoint 演示文稿（.pptx/.potx）的创建、读取、编辑与分析。涵盖幻灯片组、汇报/答辩 deck、模板套用、抽取文本、增删重排页面、演讲者备注、批注、以及把材料整理成一套演示文稿。触发词：PPT、pptx、幻灯片、演示文稿、汇报、答辩、组会 slides、模板、演讲备注、deck。"
license: "本地原创，借鉴 anthropics/skills 的 pptx 技能工作流（该技能为 source-available，本文件未复制其文本）"
---

# PPT 演示文稿处理

## 📖 说明

**独立重写版**。原版 `pptx` 技能为 source-available，不可再分发；
此处只借鉴其分层思路，内容原创。

## 零、和 docx 一样：.pptx 也是 ZIP

```
deck.pptx ──unzip──▶ ppt/presentation.xml    （幻灯片顺序 sldIdLst）
                     ppt/slides/slideN.xml    （每页内容）
                     ppt/slideLayouts/*       （版式）
                     ppt/slideMasters/*       （母版）
                     ppt/theme/*              （主题配色字体）
                     ppt/notesSlides/*        （演讲者备注）
                     ppt/media/*              （图片/视频）
```

**两条路：**

| 任务 | 做法 |
|---|---|
| 从零生成 | `python-pptx` 或 pptxgenjs |
| 改既有 deck | 解包 → 改 `slideN.xml` → 重打包 |
| 重排 / 删页 | 改 `presentation.xml` 里的 `sldIdLst` |
| 套模板 | **复制模板文件再改内容**，不要从空白重画 |

## 一、环境

```bash
python -m venv .venv && .venv/Scripts/pip install python-pptx
```

**若本机已有 `tencent-pptx` 内置技能，优先复用**——本 skill 负责选路、审美与质检。

## 二、关键策略：套模板，不要从零画

**从空白 `Presentation()` 开始做出来的 deck 一定难看**——因为它用的是
python-pptx 的默认母版，字体、配色、占位符位置都是最朴素的。

正确做法：

```python
from pptx import Presentation

# 以现成模板为基底，继承它的母版/版式/主题
prs = Presentation("template.pptx")
for layout in prs.slide_layouts:
    print(layout.name)     # 先看有哪些版式可用

slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "标题"
slide.placeholders[1].text = "正文"
prs.save("out.pptx")
```

如有现成的机构模板或主题库，直接以它为基底套用，不要从空白重画。

## 三、从零生成（无模板时）

### 设计要点

| 维度 | 建议 |
|---|---|
| 配色 | 1 主色 + 1 辅色 + 中性灰，**不超过 3 个色相** |
| 字号 | 标题 32-40pt，正文 20-24pt，**最小不低于 18pt** |
| 字体 | 中文思源黑体/微软雅黑，西文 Inter / Calibri；全篇统一 |
| 留白 | 每页内容占版心 60-70%，别塞满 |
| 每页要点 | **不超过 6 条**，超过就拆页 |
| 图表 | 能用图就别用表，能用表就别用大段文字 |

### 常见错误（逐条避开）

- ❌ 一页塞 10 个 bullet —— 拆页
- ❌ 正文 14pt —— 后排看不见
- ❌ 每页换一种配色 —— 观感碎裂
- ❌ 标题栏文字超出边界 —— 换行或缩字号
- ❌ 直接用默认蓝色主题 —— 一眼模板感

## 四、改既有 deck

```bash
unzip -o deck.pptx -d unpacked
# 改 ppt/slides/slideN.xml
cd unpacked && zip -r ../deck_new.pptx . -x '.*'
```

**重排 / 删页**：改 `ppt/presentation.xml` 的 `<p:sldIdLst>`，
按 `<p:sldId>` 顺序增删即可，**不要改文件名**。

**同 docx 的三条铁律**：不格式化 XML、用 lxml 不用正则、改完必须打开验证。

## 五、演讲者备注

```python
notes = slide.notes_slide.notes_text_frame
notes.text = "这里写讲稿提示"
```

## 六、质检清单（交付前必过）

1. **能打开**——PowerPoint / WPS 不报修复
2. **逐页目视**——渲染成图，检查有没有溢出、重叠、错位
3. **字号合格**——正文 ≥18pt
4. **配色统一**——全篇色相数 ≤3
5. **中文字体正确**——`eastAsia` 是否设置
6. **图片没丢**——`ppt/media/` 数量对得上

**渲染成图自检**（推荐）：

```bash
# LibreOffice 无头转换后逐页看图
soffice --headless --convert-to pdf deck.pptx
```

## 七、诚实性要求

- **不要声称「设计得很好看」**——审美是主观的，把设计决策（配色、
  字号、留白）说清楚，让用户自己判断。
- 模板套用时如果**某些版式没被正确继承**，如实说明，不要掩盖。
- 图片素材的**来源与授权**要交代清楚，别默认用户有权使用。
