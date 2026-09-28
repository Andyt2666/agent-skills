---
name: "doc-xlsx"
description: "电子表格（.xlsx/.xlsm/.xltx/.csv/.tsv）的创建、读取、编辑、清洗与分析。涵盖新增列、写公式、格式化、图表、数据透视、合并排序筛选、脏数据整理、以及从其他数据源生成规范表格。触发词：Excel、xlsx、表格、电子表格、CSV、数据清洗、公式、图表、透视表、整理数据、数据核对。"
license: "本地原创，借鉴 anthropics/skills 的 xlsx 技能工作流（该技能为 source-available，本文件未复制其文本）"
---

# 电子表格处理

## 📖 说明

**独立重写版**。原版 `xlsx` 技能为 source-available、不可再分发；
此处只借鉴其分层思路，内容原创。

## 零、按任务选库

| 任务 | 用什么 | 为什么 |
|---|---|---|
| 写公式 / 精细格式 | `openpyxl` | 能控制单元格级样式与公式 |
| 大批量读写数据 | `pandas` | `read_excel` / `to_excel` 快且省事 |
| 读已有文件的公式 | `openpyxl`（`data_only=False`） | pandas 读不到公式 |
| 读**计算结果** | `openpyxl`（`data_only=True`） | 需要文件被 Excel 保存过 |
| 图表 / 透视 | `openpyxl` 的 chart / pivot 模块 | |

**关键分叉**：`data_only=True` 只能读到**上次 Excel 保存时缓存的**值。
如果文件是用 openpyxl 新写的，**公式没有缓存值，读出来是 `None`**。
这不是 bug，是没重算。

## 一、环境

```bash
python -m venv .venv && .venv/Scripts/pip install openpyxl pandas
```

**若本机已有 `tencent-docs-sheetagent` / `tencent-docs-sheet-generation`
内置技能，优先复用**——本 skill 负责选路与质检。

## 二、生成与编辑

```python
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "数据"

ws["A1"] = "器件"
ws["B1"] = "价格"
ws["A2"] = "传感器 A"
ws["B2"] = 12000
ws["C2"] = "=B2*1.13"        # 写公式

# 表头样式
head = Font(bold=True, color="FFFFFF")
fill = PatternFill("solid", fgColor="2F5597")
for c in ws[1]:
    c.font = head
    c.fill = fill

ws.column_dimensions["A"].width = 18
wb.save("out.xlsx")
```

## 三、公式必须重算（最重要的一条）

openpyxl **只写公式字符串，不计算公式**。用 openpyxl 生成的文件里，
公式单元格在别的程序打开前是**没有值**的。

两种处理：

```bash
# 方案 A：用 LibreOffice 无头重算
soffice --headless --convert-to xlsx --outdir recalc/ out.xlsx
```

```python
# 方案 B：写完后用 LibreOffice 宏/CLI 打开保存一次
```

**不重算就交付 = 交付了一个公式显示为空白/0 的文件。**
这是最常见的翻车点。

## 四、公式选择（要能扛住重算与校验）

| 想做的事 | 推荐 | 避免 |
|---|---|---|
| 求和 | `SUM` / `SUMIFS` | 手写 `+` 连加 |
| 查表 | `XLOOKUP`（新版）或 `INDEX+MATCH` | `VLOOKUP`（列序敏感） |
| 条件计数 | `COUNTIFS` | `COUNTIF` 套多层 |
| 空值兜底 | `IFERROR` 包裹 | 让 `#DIV/0!` 裸露 |
| 动态数组 | 直接写溢出公式 | 旧版数组公式 `Ctrl+Shift+Enter` |

**写完公式后必做**：重算 → 扫一遍有没有 `#REF!` / `#VALUE!` / `#N/A`。

## 五、常见坑

- **日期**：Excel 日期是序列号。pandas 读进来可能是 `datetime`，
  写回去可能变成数字。显式设 `number_format`。
- **长数字串**：身份证号、订单号超过 15 位会被转成科学计数法**且丢精度**。
  必须设成文本格式：`ws["A1"].number_format = "@"`。
- **合并单元格**：`ws.merged_cells`，写值时只能写左上角那个。
  合并单元格是**下游处理的噩梦**，能不用就不用。
- **前导零**：`007` 会变 `7`，同样要设文本格式。
- **pandas 写多 sheet**：用 `pd.ExcelWriter`，注意 `mode="a"` 追加时
  需要 `if_sheet_exists="replace"`。

## 六、质检清单

1. **公式有值**——重算后没有空白/`#N/A`
2. **数字没变科学计数**——长数字串抽查
3. **日期显示正常**——不是 45000 这种序列号
4. **表头与列宽可读**——没有 `####` 挤在一起
5. **sheet 名与数量对**——别多出默认的 `Sheet1`

## 七、诚实性要求

- **数据不准就说数据不准**。清洗掉的行数、丢弃的异常值，
  必须给出具体数字和理由，不能悄悄删。
- **公式没重算就直说**「需在 Excel 中打开一次以计算」。
- 涉及**金额、报价、器件参数**时，单位（元/美元、含税/不含税）
  必须逐列标注清楚——在器件选型表场景里尤其重要。
