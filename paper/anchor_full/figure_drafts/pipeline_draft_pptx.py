"""Editable draft of a revised pipeline figure (Fig. 3), 2026-11-09.

Slide 1: the proposed figure. Every header, caption, formula box and arrow is a native PowerPoint shape and can be
edited; the panels taken over from the collaborator's figure (figures/anchor_framework.pptx, rendered PDF) are pictures,
and the two new sketches (bound region, output map with per-frame record) are pictures generated from saved data.
Slide 2: what changed and why (Chinese notes for the authors).
Run:  python pipeline_draft_pptx.py <dir with input.png extract.png layout.png mapping.png bound_sketch.png output_sketch.png> <out.pptx>
Needs python-pptx (a scratch environment is enough).
"""
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

SRC = Path(sys.argv[1]); OUT = Path(sys.argv[2])
INK = RGBColor(0x22, 0x22, 0x22); GREY = RGBColor(0xF0, 0xF1, 0xF3); EDGE = RGBColor(0x9A, 0xA1, 0xA8)
BLUE = RGBColor(0x00, 0x72, 0xB2); NEW = RGBColor(0xFF, 0xF4, 0xE0); NEWEDGE = RGBColor(0xE0, 0x82, 0x14)
FONT = 'Times New Roman'

prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(6.2)
s = prs.slides.add_slide(prs.slide_layouts[6])


def box(x, y, w, h, fill=None, edge=EDGE, width=0.75):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.shadow.inherit = False
    if fill is None: sh.fill.background()
    else: sh.fill.solid(); sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = edge; sh.line.width = Pt(width)
    return sh


def text(x, y, w, h, lines, size=11, bold=False, align=PP_ALIGN.CENTER, color=INK, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor
    for k, ln in enumerate(lines if isinstance(lines, list) else [lines]):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph(); p.alignment = align
        r = p.add_run(); r.text = ln; r.font.size = Pt(size); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = color
    return tb


def picture(name, x, y, w=None, h=None):
    im = Image.open(SRC / name); ar = im.height / im.width
    if w is not None and h is not None:
        if w * ar > h: w = h / ar
        else: h = w * ar
    elif w is not None: h = w * ar
    else: w = h / ar
    return s.shapes.add_picture(str(SRC / name), Inches(x), Inches(y), Inches(w), Inches(h)), w, h


def arrow(x0, y0, x1, y1, color=BLUE):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x0), Inches(y0), Inches(x1), Inches(y1))
    c.line.color.rgb = color; c.line.width = Pt(1.5)
    ln = c.line._get_or_add_ln(); from pptx.oxml.ns import qn
    tail = ln.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'med', 'len': 'med'}); ln.append(tail)
    return c


# title
text(0.2, 0.05, 12.9, 0.4, 'AnchorMTM: from a field sequence and one budget ε to a map whose axis is a direction in space', 15, True)
# columns: (x, w, header, is_new)
COL = [(0.15, 1.45, 'Input', False), (1.75, 2.25, '(1) Trees and reference', False), (4.15, 1.85, '(2) Price of the axis', True),
       (6.15, 2.45, '(3) Leaf order and anchors', False), (8.75, 2.45, '(4) Profiles and checks', False), (11.35, 1.85, 'Output', True)]
Y0, H = 0.55, 5.55
for x, w, head, new in COL:
    box(x, Y0, w, H, fill=None, edge=NEWEDGE if new else EDGE, width=1.25 if new else .75)
    box(x, Y0, w, 0.42, fill=NEW if new else GREY, edge=NEWEDGE if new else EDGE, width=1.25 if new else .75)
    text(x, Y0 + .04, w, .36, head, 12.5, True)

# Input
text(0.15, 1.05, 1.45, 0.35, 'F(x, t), budget ε', 11.5, True)
picture('input.png', 0.3, 1.45, w=1.15, h=3.2)
text(0.15, 4.75, 1.45, 1.2, ['Scalar fields of all', 'time steps; one number', 'ε ≥ 0 (merge-error budget)'], 9)
# (1)
picture('extract.png', 1.85, 1.05, w=2.05, h=3.75)
text(1.75, 4.85, 2.25, 1.15, ['Merge trees Tₜ, leaf supports', 'matched over time, one direction a*;', 'reference qᵢ = ⟨a*, pᵢ⟩ − o'], 9)
# (2) new: bounds
text(4.15, 1.05, 1.85, 0.3, 'from T, q, W only', 10, False, color=NEWEDGE)
text(4.2, 1.35, 1.75, 1.25, ['ν*(T, q)   exact tree', 'B_w(T, q, W)   widths', 'C_η(T, q)   merge error ≤ η'], 10, align=PP_ALIGN.LEFT)
picture('bound_sketch.png', 4.25, 2.6, w=1.65)
text(4.15, 4.35, 1.85, 1.65, ['Known before any layout:', 'how much displacement the', 'tree forces, where in the tree,', 'and how much merge error', 'releases it.'], 9)
# (3) order + placement
picture('layout.png', 6.25, 1.0, w=2.25, h=3.0)
box(6.25, 4.05, 2.25, 0.62, fill=RGBColor(0xEE, 0xF5, 0xFB), edge=BLUE)
text(6.25, 4.07, 2.25, 0.6, ['admit π if δ*(π) ≤ η (closed form)', 'choose least τ(π), then NROE'], 9)
text(6.15, 4.75, 2.45, 1.25, ['Anchors: convex QP with', '‖x − q‖∞ ≤ τ(π) + β₀;', 'η = 0 keeps the blocks, η > 0 admits', 'an order that follows q'], 9)
# (4) profiles + checks
picture('mapping.png', 8.85, 1.0, w=2.25, h=3.0)
box(8.85, 4.05, 2.25, 0.62, fill=RGBColor(0xEE, 0xF5, 0xFB), edge=BLUE)
text(8.85, 4.07, 2.25, 0.6, ['barriers bₖ = Cₖ + δ*(π)', 'check d_top ≤ η on every frame'], 9)
text(8.75, 4.75, 2.45, 1.25, ['Leaf-arc samples and LCA paths', 'fill each profile ψₜ; profiles share', 'origin, direction and scale'], 9)
# Output
picture('output_sketch.png', 11.45, 1.0, w=1.7, h=3.75)
text(11.35, 4.75, 1.85, 1.25, ['Map I(t, u) = ψₜ(u) with', 'marked barriers, and per frame:', 'bound, τ, displacement, merge', 'error within ε'], 9)
# arrows
for (x, w, *_), (x2, *__) in zip(COL[:-1], COL[1:]):
    arrow(x + w + .01, 3.0, x2 - .01, 3.0)
arrow(5.075, 4.3, 5.075, 4.3)  # placeholder removed below
s.shapes._spTree.remove(s.shapes[-1]._element)
# dashed link: bounds inform the order choice
c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(5.95), Inches(2.0), Inches(6.2), Inches(4.3))
c.line.color.rgb = NEWEDGE; c.line.width = Pt(1); c.line.dash_style = 4

# slide 2: notes
s2 = prs.slides.add_slide(prs.slide_layouts[6]); s = s2
text(0.4, 0.3, 12.5, 0.5, '修改说明（草稿，供作者修订）', 16, True, align=PP_ALIGN.LEFT)
notes = [
    '1. 原图流程是对的：输入场 → 提取树与参考 → 拓扑预算下的布局 → 一维剖面 → 地图；示意里的叶序 A,C,B,D 与图 2、图 4 一致。',
    '2. 原图缺两步，而这两步正是论文的核心：(a) 下界——只用 T、q、W 就能算出，画图之前就知道代价；(b) 预算的闭式检验 δ*(π) ≤ η 与渲染后的逐帧核验。',
    '3. 新增第 (2) 列"Price of the axis"（橙色框）：列出 ν*、B_w、C_η，配一张与图 5 同样画法的"不可达区域"小图；虚线表示下界指导第 (3) 步的叶序选择。',
    '4. 第 (3) 列改名为"Leaf order and anchors"，在原图下加闭式检验和选择规则（δ* ≤ η，最小 τ），并写出放置的上限 ‖x−q‖ ≤ τ+β₀。',
    '5. 第 (4) 列改名为"Profiles and checks"，加屏障公式和逐帧核验 d_top ≤ η。',
    '6. Output 列不再空：上面是带标记屏障的地图（Storms，ε=10%，黄色为改变的屏障），下面是逐帧记录（位移与合并误差，虚线为预算）。这对应论文的说法"每帧都报告实际花掉的合并误差"。',
    '7. 所有标题、说明文字、公式框和箭头都是可编辑的 PowerPoint 形状；原图各列是图片，新的两张小图由保存数据生成（脚本 pipeline_draft_pptx.py）。',
    '8. 若采纳：建议在合作者的 anchor_framework.pptx 里按本稿重排，保持原有配色与字体，并把正文图注改成四步：(1) 提取与参考 (2) 位置代价 (3) 叶序与锚点 (4) 剖面与核验。',
]
text(0.5, 0.95, 12.3, 5, notes, 12.5, align=PP_ALIGN.LEFT)
prs.save(OUT); print('saved', OUT)
