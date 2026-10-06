# 设计系统：令牌、对比度与字体排印

> [English](../en/design_system.md) | 简体中文

一份演示文稿的外观来自一份**设计令牌 (design tokens)** 文件：可以是 `presets/` 里的四个预设之一，也可以是 `cli.py undo` 对真实模板的抽取结果。本页说明令牌包含什么，以及无论令牌写了什么，引擎都保证什么。

## 令牌字段

| 字段 | 含义 |
| :--- | :--- |
| `theme_mode` | `light` 或 `dark` |
| `palette.background / surface / surface_subtle / border` | 页面底色、卡片、次要卡片、卡片描边 |
| `palette.text_primary / text_secondary` | 正文与辅助文字 |
| `palette.primary / secondary / accent` | 品牌色（填充、徽标、图表系列） |
| `typography.title / subtitle / body / kpi_number` | `font`、`size`、`color` |
| `typography.font_ea` | 中日韩文字使用的东亚字体（取自主题，否则为 PingFang SC） |
| `card_style.border_radius` | 圆角半径，单位 px（96 px = 1 英寸） |
| `canvas.margin_left_inches / margin_top_inches` | `undo` 会把它限制在 0.8 英寸内；页眉使用的边距不会超过 1.0 英寸 |
| `theme_source` | `undo` 读到了什么：配色方案名、母版背景、主题字体 |
| `design_notes` | 设计检查所做的修正 |

## 保证

1. **对比度。** 每一个文字都对其背后的填充色达到 4.5:1（18pt 及以上，或 14pt 粗体及以上的文字为 3:1）。不达标的颜色会沿原色相向黑或白调整。填充从不被改动，所以用作徽标或表头填充的品牌色保持原样，其上的文字自动换成白色或近黑。
2. **字号下限。** 小于 12pt 的文字在卡片放得下时被抬高到 12pt；放不下时保持不动（此时版面 lint 会报告溢出，而不是让文字悄悄缩小）。
3. **单行页眉。** 标题会缩小（最小到 22pt）直到能放进一行；模板里大于 34pt 的标题字号和大于 18pt 的副标题字号，会被限制到版式网格为页眉预留的高度。
4. **粗体字体。** 本身已经很粗的字体（Impact、Haettenschweiler、名字里带 Black 或 Heavy 的）不再叠加合成加粗。

## 检查令牌

```python
from core.design_check import check_tokens, repair_tokens
findings = check_tokens(tokens)          # TOKEN_LOW_CONTRAST、TOKEN_SIZE_TOO_SMALL、TOKEN_WEAK_HIERARCHY
fixed, notes = repair_tokens(tokens)     # 保持色相、调整明度；抬高字号；不改入参
```

`palette.primary` 不作为文字色校验：它是主要用作填充的品牌色，用作文字的那些文字，由版式阶段逐个修复。

## 套用企业模板

```bash
python3 cli.py undo --template company.pptx --out .undoppt/design_tokens.json
python3 cli.py build --blueprint .undoppt/blueprint.json --tokens .undoppt/design_tokens.json
python3 cli.py render-check --pptx output/presentation.pptx --render
```

会带过来的：配色、明暗模式、字体（包括东亚字体）。不会带过来的：模板的母版版式、背景图与 logo 不会放到生成的页面上（构建器自己绘制 16:9 版式），4:3 的模板按 16:9 输出。
