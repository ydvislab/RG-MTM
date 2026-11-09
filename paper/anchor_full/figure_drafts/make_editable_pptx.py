"""Editable PowerPoint of every figure of paper 1037 v33 (Figs. 1-10) and its supplement (Figs. S1-S4), 2026-11-09.

Each slide holds one figure exactly as the paper uses it: an SVG converted from the figure PDF (text kept as text) with a
300-dpi PNG fallback. In PowerPoint 365: right-click the picture -> Convert to Shape, and every line, marker and label
becomes an editable shape (embedded raster maps stay pictures). The overlays that LaTeX draws on Figs. 1 and 9 (tikz)
are added as native PowerPoint shapes at the same relative positions. Speaker notes give the source file of each figure.
Usage: python make_editable_pptx.py OUT.pptx
"""
import subprocess, sys, tempfile
from pathlib import Path
import pymupdf
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.opc.package import Part
from pptx.opc.packuri import PackURI
from pptx.opc.constants import RELATIONSHIP_TYPE as RT

FIG = Path(__file__).resolve().parents[2] / 'pvis2027/latex_v30/figures'
SLIDE_W, SLIDE_H = 13.333, 7.5
# (label, title, [pdf files stacked], print width in inches, overlay)
FIGS = [
    ('Fig. 1', 'Storms temporal overview (teaser)', ['anchor_storms_overview'], 7.05, 'fig1'),
    ('Fig. 2', 'Mapping strategies on a common 35-sample field', ['anchor_related_work_mapping', 'anchor_related_work_panel_d'], 3.42, None),
    ('Fig. 3', 'Augmented merge tree and its profile', ['anchor_node_mapping'], 3.42, None),
    ('Fig. 4', 'AnchorMTM workflow', ['anchor_framework'], 7.05, None),
    ('Fig. 5', 'Selective flattening', ['anchor_relaxation_open'], 3.42, None),
    ('Fig. 6', 'Forced and chosen order error', ['forced_plane'], 7.05, None),
    ('Fig. 7', 'Feature positions on Tangaroa and Cylinder', ['volume_gallery'], 6.63, None),
    ('Fig. 8', 'Where a merge budget acts', ['budget_response_v30'], 7.05, None),
    ('Fig. 9', 'Storms event window at five budgets', ['anchor_storms_budget_maps'], 7.05, 'fig9'),
    ('Fig. 10', 'Cylinder, central-tree variant', ['anchor_cylinder_centered_blue'], 7.05, None),
    ('Fig. S1', 'Leaf correspondence', ['anchor_leaf_correspondence'], 5.08, None),
    ('Fig. S2', 'The budget sampled finely', ['supp_budget_sweep'], 7.05, None),
    ('Fig. S3', 'Cylinder in three maps', ['supp_cylinder_compare'], 7.05, None),
    ('Fig. S4', 'Hourly PM2.5 in three maps', ['supp_pm25_compare'], 7.05, None),
]
SVG_EXT = '{96DAC541-7B7A-43D3-8B79-37D633B846F1}'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS_SVG = 'http://schemas.microsoft.com/office/drawing/2016/SVG/main'


def convert(stem, tmp):
    doc = pymupdf.open(FIG / f'{stem}.pdf'); page = doc[0]
    svg = page.get_svg_image(text_as_path=False).encode('utf-8')
    png = Path(tmp) / f'{stem}.png'
    subprocess.run(['pdftoppm', '-r', '300', '-png', '-singlefile', str(FIG / f'{stem}.pdf'), str(png.with_suffix(''))], check=True)
    return svg, png, page.rect.width / page.rect.height


def add_svg_picture(slide, svg, png, x, y, w, h, n):
    pic = slide.shapes.add_picture(str(png), Inches(x), Inches(y), Inches(w), Inches(h))
    part = Part(PackURI(f'/ppt/media/figure_svg{n}.svg'), 'image/svg+xml', slide.part.package, svg)
    rid = slide.part.relate_to(part, RT.IMAGE)
    blip = pic._element.xpath('.//a:blip')[0]
    ext_lst = etree.SubElement(blip, f'{{{NS_A}}}extLst'); ext = etree.SubElement(ext_lst, f'{{{NS_A}}}ext'); ext.set('uri', SVG_EXT)
    svgb = etree.SubElement(ext, f'{{{NS_SVG}}}svgBlip', nsmap={'asvg': NS_SVG}); svgb.set(f'{{{NS_R}}}embed', rid)
    return pic


def text(slide, s, x, y, size, bold=False, anchor='center', w=2.5, h=.3):
    tb = slide.shapes.add_textbox(Inches(x - (w / 2 if anchor == 'center' else 0)), Inches(y - h / 2), Inches(w), Inches(h))
    tf = tb.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER if anchor == 'center' else PP_ALIGN.LEFT
    r = p.add_run(); r.text = s; r.font.size = Pt(size); r.font.bold = bold; r.font.name = 'Times New Roman'
    return tb


def overlay(slide, kind, x0, y0, w, h, scale):
    X = lambda u: x0 + u * w; Y = lambda v: y0 + (1 - v) * h          # figure coordinates (origin bottom left)
    fs = 8 * scale                                                     # \footnotesize at print size
    if kind == 'fig1':
        ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(X(.94)), Inches(Y(.13)), Inches(X(.94)), Inches(Y(.325)))
        ln.line.width = Pt(.9 * scale); ln.line.color.rgb = RGBColor(0x33, 0x33, 0x33)
        ln.line._get_or_add_ln().append(etree.fromstring(f'<a:tailEnd xmlns:a="{NS_A}" type="triangle"/>'))
        for s, v in (('W', .14), ('E', .315), ('a*', .2275)):
            text(slide, s, X(.947), Y(v), fs, anchor='left', w=.5, h=.25)
    if kind == 'fig9':
        for (a, b, c, d), (t1, t2), cx in [((.5329, .3089, .6803, .4051), ('Relative geometry', '+ pairwise distances'), .6066),
                                           ((.1711, .3049, .3133, .4038), ('Fixed spatial axis', '+ merge budget'), .2422)]:
            box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(X(a)), Inches(Y(d)), Inches((c - a) * w), Inches((d - b) * h))
            box.fill.solid(); box.fill.fore_color.rgb = RGBColor(255, 255, 255); box.line.fill.background()
            text(slide, t1, X(cx), Y(.378), fs, bold=True, w=(c - a) * w, h=.25)
            text(slide, t2, X(cx), Y(.3374), fs, w=(c - a) * w, h=.25)


def main(out):
    prs = Presentation(); prs.slide_width = Inches(SLIDE_W); prs.slide_height = Inches(SLIDE_H)
    blank = prs.slide_layouts[6]; n = 0
    with tempfile.TemporaryDirectory() as tmp:
        for label, title, stems, print_w, ov in FIGS:
            s = prs.slides.add_slide(blank)
            text(s, f'{label}  {title}', .5, .45, 20, bold=True, anchor='left', w=12, h=.5)
            parts = [convert(st, tmp) for st in stems]
            aspect = 1 / sum(1 / a for _, _, a in parts)               # stacked: total height = sum of heights
            W = min(12.3, 6.4 * aspect); H = W / aspect; x = (SLIDE_W - W) / 2; y = .9 + (6.4 - H) / 2
            for svg, png, a in parts:
                n += 1; hh = W / a; add_svg_picture(s, svg, png, x, y, W, hh, n)
                if ov: overlay(s, ov, x, y, W, hh, W / print_w)
                y += hh
            s.notes_slide.notes_text_frame.text = (f'{label}: ' + ', '.join(f'figures/{st}.pdf' for st in stems)
                                                   + '. Right-click the picture, Convert to Shape, to edit it.')
    prs.save(out); print('saved', out, n, 'pictures')


if __name__ == '__main__':
    main(sys.argv[1])
