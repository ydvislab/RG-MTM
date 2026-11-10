# 论文 1037 v34 全部配图的可编辑 PPT（2026-11-09）

每张图一个 PPT，幻灯片大小等于图的印刷尺寸。图号是 v34 的图号；因为合作者 zip 里还保留着节点映射和 Cylinder 两张图，所以它的编号不同，对照见下表。

| 文件 | v34 图号 | 合作者 zip 图号 | 内容 | 来源 |
|---|---|---|---|---|
| `Fig1_storms_overview.pptx` | 图 1 | 图 1 | Storms 总览 | 合作者 PPT，原样 |
| `Fig2_workflow.pptx` | 图 2 | 图 3 | 流程图 | 合作者 PPT，原样 |
| `Fig3_selective_flattening.pptx` | 图 3 | 图 4 | 选择性压平 | 合作者 PPT，原样 |
| `Fig4_forced_error.pptx` | 图 4 | 图 5 | 强制与选择误差 | 由 PDF 转成原生对象 |
| `Fig5_volume_positions.pptx` | 图 5 | 图 6 | 体数据特征位置 | 由 PDF 转成原生对象 |
| `Fig6_budget_response.pptx` | 图 6 | 图 7 | 预算在各帧的作用 | 由 PDF 转成原生对象 |
| `Fig7_storms_budget_maps.pptx` | 图 7 | 图 8 | Storms 事件窗口 | 合作者 PPT，原样 |
| `FigS1_linearization_strategies.pptx` | 图 S1 | 原图 2 的 (a–c) | 三种线性化策略 | 合作者 PPT，原样 |
| `FigS2_node_mapping.pptx` | 图 S2 | 图 2 | 增广树与剖面 | 合作者 PPT，原样 |
| `FigS3_leaf_correspondence.pptx` | 图 S3 | 图 S1 | 叶对应 | 合作者 PPT，原样 |
| `FigS4_budget_sweep.pptx` | 图 S4 | 图 S2 | 细预算扫描 | 由 PDF 转成原生对象 |
| `FigS5_cylinder_variant.pptx` | 图 S5 | 图 9 | Cylinder 变体 | 合作者 PPT，原样 |
| `FigS6_cylinder_three_maps.pptx` | 图 S6 | 图 S3 | Cylinder 三种地图 | 由 PDF 转成原生对象 |
| `FigS7_pm25_compare.pptx` | 图 S7 | 图 S4 | PM2.5 三种地图 | 由 PDF 转成原生对象 |

## 由 PDF 转成的六张图怎么编辑
- 坐标轴、刻度、折线、柱和标记都是 PowerPoint 原生对象，可以直接改颜色、线宽和位置。
- 文字是真实文本框（Times New Roman），字号与原图相同，可以直接改字。
- 带颜色的地图和散点云是图片，可以移动、缩放或替换，但不能改单个像素或点。
- 图 4 的斜线区域用的是 PowerPoint 的图案填充，可在“设置形状格式”里修改。

## 版本说明
- `Fig1`、`Fig2`、`Fig3`、`Fig7`、`FigS2`、`FigS3`、`FigS5` 是合作者 v34 zip 里的最新版，v36 已替换进 `paper/pvis2027/latex_v30/figures/`。
- `Fig4`、`Fig5`、`Fig6` 已按 v36 重新生成，与 `paper/1037_v36.pdf` 一致：Tangaroa 沿流向 x 轴，不含 Gaussian；图 4 加了 NPE 一行，图 5 用柱状图报告误差。

重新生成：
```bash
python3 paper/anchor_full/figure_drafts/pdf_to_native_pptx.py IN.pdf OUT.pptx
```
