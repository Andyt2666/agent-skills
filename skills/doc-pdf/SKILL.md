---
name: "doc-pdf"
description: "PDF 文件的读、拆、合、改、填、转。涵盖文本与表格抽取、合并/拆分/旋转、加水印、表单填写、加密解密、图片抽取、扫描件 OCR、以及从零生成 PDF。触发词：PDF、pdf 文件、合并 PDF、拆分 PDF、PDF 表单、填表、抽取表格、OCR、扫描件、加水印、加密、生成 PDF。"
license: "本地原创，借鉴 anthropics/skills 的 pdf 技能工作流（该技能为 source-available，本文件未复制其文本）"
---

# PDF 处理

## 📖 说明

本 skill 是**独立重写版**：只借鉴了 Anthropic 官方 `pdf` 技能的**任务分层思路**，
正文与代码示例均为本地原创，不含其原始文本。原版为 source-available 许可、
不可再分发，因此这里不克隆、只重写。

## 零、先定任务类型

PDF 任务的解法差异极大，**先归类再选工具**，不要一上来就写代码。

| 任务 | 首选工具 | 备注 |
|---|---|---|
| 纯文本抽取 | `pypdf` 或 `pdfplumber` | 有版式的用 pdfplumber |
| 表格抽取 | `pdfplumber` | 复杂表格需按 `extract_table` 的线框参数调 |
| 合并 / 拆分 / 旋转 | `pypdf` | 纯结构操作，别用 OCR |
| 加水印 / 页眉页脚 | `reportlab` + `pypdf` 叠加 | 先造水印层再 merge |
| 表单填写 | `pypdf` 的 `update_page_form_field_values` | 需 `NeedAppearances` |
| 加密 / 解密 | `pypdf` 的 `encrypt` / `decrypt` | AES 需 `cryptography` |
| 图片抽取 | `pypdf` 的 `page.images` | 或 `pdfimages` |
| 扫描件 OCR | `ocrmypdf`（底层 Tesseract） | 中文需 `chi_sim` 语言包 |
| 从零生成 | `reportlab`（精确排版）或 HTML→PDF | 见第五节 |

**如果本机已有 `pdfkit-py` / `pdf` 内置技能**：优先复用，本 skill 负责**决策与质检**，
避免重复实现。

## 一、环境准备

```bash
# 建议装在独立 venv，不污染全局
python -m venv .venv && .venv/Scripts/pip install \
  pypdf pdfplumber reportlab ocrmypdf
```

中文 OCR 额外需要：

```bash
# Windows 下 Tesseract 需单独安装并加 chi_sim 语言包
tesseract --list-langs   # 确认有 chi_sim
```

**没有 `chi_sim` 就别声称能 OCR 中文**——先装上再说，或者明确告知用户做不到。

## 二、文本与表格抽取

```python
import pdfplumber

with pdfplumber.open("in.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"--- page {i+1} ---")
        print(page.extract_text())
        for t in page.extract_tables():
            print(t)
```

**常见坑：**

- **双栏论文**：`extract_text()` 会按 y 坐标交错，读出来是乱的。
  双栏要按 `page.crop((x0, 0, x1, h))` 分左右两半分别抽。
- **表格无线框**：`extract_tables()` 默认靠线框；无线框需传
  `table_settings={"vertical_strategy": "text", "horizontal_strategy": "text"}`。
- **公式**：PDF 里的公式基本抽不出来（是字形不是文本），
  别浪费时间，直接当图片处理。

## 三、合并 / 拆分 / 旋转

```python
from pypdf import PdfReader, PdfWriter

w = PdfWriter()
for f in ["a.pdf", "b.pdf"]:
    for p in PdfReader(f).pages:
        w.add_page(p)
w.write("merged.pdf")
```

拆分与旋转同理，都是 `PdfWriter` + `add_page` / `page.rotate(90)`。

## 四、表单填写

```python
from pypdf import PdfReader, PdfWriter

r = PdfReader("form.pdf")
w = PdfWriter(clone_from=r)
w.update_page_form_field_values(w.pages[0], {"name": "Zhang San", "date": "2026-09-23"})

# 关键：不设这个，部分阅读器看不到填进去的值
w.set_need_appearances_writer(True)
w.write("filled.pdf")
```

**先探明字段名**：`r.get_fields()` 打印出所有 field 的键，
不要猜字段名。

## 五、从零生成

| 方式 | 适用 | 代价 |
|---|---|---|
| `reportlab` canvas | 精确坐标排版、批量出图 | 排版要手算，但可控 |
| `reportlab` platypus | 流式文档、表格、段落 | 上手快，细节受限 |
| HTML → PDF | 已有网页/富文本 | 需 Playwright / weasyprint |

**中文必须显式注册字体**，否则全是方块：

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("CN", "C:/Windows/Fonts/msyh.ttc"))
```

## 六、质检清单（交付前必过）

1. **页数对不对**——`len(PdfReader(out).pages)` 与预期一致
2. **中文没变方块**——随机抽一页渲染成图看一眼
3. **表单值真的可见**——用非 Acrobat 的阅读器（如浏览器）打开验证
4. **文件能打开**——不是 0 字节，不是损坏的交叉引用表
5. **没有把扫描件当文本处理**——`extract_text()` 返回空 → 那是图片，走 OCR

## 七、诚实性要求

- 抽取结果**不准就是不准**：双栏错行、公式丢失、表格错列，
  必须如实告诉用户，不能交一份看着完整实则错乱的文本。
- OCR 的**字符准确率不要瞎报**。低质量扫描件直接说明「识别质量有限，
  建议人工校对关键字段」。
- 加密 PDF 解不开时，说清是**权限口令**还是**用户口令**的问题，
  不要反复尝试。
