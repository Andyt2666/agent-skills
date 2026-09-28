---
name: "research-figure-spec"
description: "科研图表的规范与制作：期刊投稿要求、矢量输出、字号与线宽、配色可访问性、误差棒与标注、多子图排版。适用于论文插图、答辩图表、组会图、把仿真结果出成可发表的图。触发词：科研图表、论文插图、figure、出图、矢量图、误差棒、配色、子图、matplotlib、期刊要求、投稿图。"
license: "本地原创"
---

# 科研图表规范

## 📖 说明

科研图的目标不是「好看」，是**信息密度高且不失真**。
一张合格的论文插图要能：被审稿人一眼读懂、被印刷后仍清晰、
被色盲读者正确区分。

## 一、期刊投稿硬要求（通用）

| 项 | 要求 |
|---|---|
| 格式 | **矢量优先**：PDF / EPS / SVG；位图 ≥300 dpi（线条图 ≥600 dpi） |
| 宽度 | 单栏 ~8.5 cm，双栏 ~17 cm（按目标期刊实际值） |
| 字号 | 图内文字 7-9 pt，**缩放后不小于 6 pt** |
| 线宽 | 数据线 1-1.5 pt，坐标轴线 0.5-0.75 pt |
| 字体 | Arial / Helvetica（无衬线），与正文一致 |
| 颜色 | 彩色图需保证**灰度打印可区分** |

**投稿前必查目标期刊的 Author Guidelines**——具体要求差异很大，
不要用通用规则硬套。

## 二、配色：不要用 jet / rainbow

**彩虹色图（jet / rainbow）是科研可视化里最常见的错误**：
亮度不单调，人眼会把不存在的边界看成结构。

| 场景 | 推荐 colormap |
|---|---|
| 顺序数据 | `viridis` / `magma` / `cividis` |
| 发散数据（正负） | `RdBu_r` / `coolwarm`（中心必须为 0） |
| 分类数据 | 定性色板，**最多 8 类**，超出就换图形编码 |

**色盲友好**：约 8% 男性有红绿色盲。红/绿对比是禁忌。
用 `cividis`，或用「色相 + 线型 + 标记」三重编码。

```python
import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica"],
    "font.size": 8,
    "axes.linewidth": 0.75,
    "lines.linewidth": 1.2,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "savefig.bbox": "tight",
    "savefig.dpi": 600,
    "pdf.fonttype": 42,      # 关键：字体嵌入为 TrueType，避免期刊拒稿
    "ps.fonttype": 42,
})
```

**`pdf.fonttype = 42` 这条不能漏**——很多期刊明确要求字体可编辑嵌入，
默认的 Type 3 会被拒。

## 三、必须有的元素

- [ ] **坐标轴标签带单位**（`Wavelength (nm)`，不是 `Wavelength`）
- [ ] **误差棒**（有重复测量就必须给）
- [ ] **图例**（不要靠正文解释颜色）
- [ ] **刻度向内**（`direction="in"`，期刊惯例）
- [ ] **子图标注** `(a) (b) (c)`，位置统一
- [ ] 对数轴要标明底数

## 四、误差与不确定度

| 情况 | 怎么表达 |
|---|---|
| 多次测量 | 误差棒 = 标准差 或 标准误，**图注里写清是哪个** |
| 系统误差为主 | 用误差带（band），不要用误差棒 |
| 拟合参数 | 给值 ± 拟合不确定度 |
| 样本量小 | 别用标准差冒充置信区间 |

**图注必须写清误差棒代表什么**——「error bars denote 1 SD (n=5)」
这样一句话，比任何美化都重要。

## 五、多子图排版

```python
fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.5), constrained_layout=True)
for ax, tag in zip(axes.flat, "abcd"):
    ax.set_xlabel("...")
    ax.text(-0.15, 1.05, f"({tag})", transform=ax.transAxes,
            fontweight="bold", va="top")
```

- **尺寸先按目标宽度定**（如双栏 7 inch），不要先画大再缩
- 子图之间共享轴时用 `sharex` / `sharey`，省重复标签
- 导出 PDF 交给排版，不要导出 PNG 再插进 Word

## 六、常见坑

- **截图当图用**——分辨率不够，印刷糊成一团
- **Excel 默认图直接投**——字号、配色、线宽全不合规
- **中文字体缺失**——matplotlib 中文显示方块，需显式设
  `font.sans-serif` 含 `Microsoft YaHei`，并 `axes.unicode_minus = False`
- **颜色靠 RGB 硬编码**——换主题就崩，用语义化色板

## 七、诚实性要求

- **不许修饰数据**。不做「为了好看」的平滑、截断坐标轴、删点。
  坐标轴不从 0 开始必须在图注说明。
- **不许事后挑图**。多次尝试后选最好看的那张 = 选择性报告。
- 仿真图与实验图**必须区分标注**，不能让读者以为仿真结果是实测。
- 图注里参数同样遵循 **A/B/C 三级来源标注**（实测 / 论文值 / 理论假设）。

## 八、输出

- 矢量图：`.pdf`（投稿）+ `.svg`（后续编辑）
- 位图：`.png` @ 600 dpi（预览 / 答辩 PPT）
- 附一份 `figure_notes.md`：数据来源、绘图脚本、参数表
