"""Convert a vector PDF figure into a one-slide PPTX of native PowerPoint objects (v34, 2026-11-09).

Lines become line objects, markers ellipses or freeforms, areas freeforms, text real text boxes (one per text line, Times New
Roman, original size), and raster maps pictures that can be moved or replaced. The slide has the printed size of the figure.
Clip rectangles of the PDF are applied to the geometry, so curves do not run past their axes.
Usage (repository root):  python3 paper/anchor_full/figure_drafts/pdf_to_native_pptx.py IN.pdf OUT.pptx [AREAHEX,HATCHHEX]
Needs pymupdf and python-pptx.
"""
import io, math, sys
from pathlib import Path
from xml.sax.saxutils import escape
import pymupdf
from pptx import Presentation
from pptx.util import Emu
from pptx.oxml import parse_xml

E = 12700
NS = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
ASC = .891   # ascent of Times New Roman, em


def emu(v): return int(round(v * E))
def hexc(c): return '%02X%02X%02X' % tuple(max(0, min(255, round(255 * x))) for x in c)


PATTERN = None   # (area colour hex, hatch colour hex): such areas get a native diagonal pattern fill


def fill_xml(c, op):
    if c is None: return '<a:noFill/>'
    if PATTERN and hexc(c) == PATTERN[0]:
        return f'<a:pattFill prst="wdUpDiag"><a:fgClr><a:srgbClr val="{PATTERN[1]}"/></a:fgClr><a:bgClr><a:srgbClr val="{PATTERN[0]}"/></a:bgClr></a:pattFill>'
    a = '' if op is None or op >= .999 else f'<a:alpha val="{int(op * 100000)}"/>'
    return f'<a:solidFill><a:srgbClr val="{hexc(c)}">{a}</a:srgbClr></a:solidFill>'


def line_xml(d):
    c, w = d.get('color'), d.get('width')
    if c is None or not w: return '<a:ln><a:noFill/></a:ln>'
    cap = {0: 'flat', 1: 'rnd', 2: 'sq'}.get((d.get('lineCap') or (0,))[0], 'flat')
    dash = ''
    s = (d.get('dashes') or '').strip()
    if s.startswith('[') and s[1:s.index(']')].strip():
        v = [float(x) for x in s[1:s.index(']')].split()]
        if len(v) % 2: v = v * 2
        dash = '<a:custDash>' + ''.join(f'<a:ds d="{max(1000, int(v[i] / w * 100000))}" sp="{max(1000, int(v[i + 1] / w * 100000))}"/>' for i in range(0, len(v), 2)) + '</a:custDash>'
    return f'<a:ln w="{max(1, emu(w))}" cap="{cap}">{fill_xml(c, d.get("stroke_opacity"))}{dash}<a:round/></a:ln>'


def subpaths(d):
    subs, cur, last = [], None, None
    def begin(p):
        nonlocal cur
        if cur is None or last is None or abs(p[0] - last[0]) > .01 or abs(p[1] - last[1]) > .01:
            cur = dict(start=p, seg=[], closed=False); subs.append(cur)
    for it in d['items']:
        if it[0] == 'l':
            a, b = tuple(it[1]), tuple(it[2]); begin(a); cur['seg'].append(('l', b)); last = b
        elif it[0] == 'c':
            a = tuple(it[1]); begin(a); cur['seg'].append(('c', tuple(it[2]), tuple(it[3]), tuple(it[4]))); last = tuple(it[4])
        elif it[0] in ('re', 'qu'):
            if it[0] == 're': r = it[1]; P = [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)]
            else: q = it[1]; P = [tuple(q.ul), tuple(q.ur), tuple(q.lr), tuple(q.ll)]
            cur = dict(start=P[0], seg=[('l', p) for p in P[1:]], closed=True); subs.append(cur); last = None
    for s in subs:
        if s['seg'] and d.get('closePath'): s['closed'] = True
        e = s['seg'][-1][-1] if s['seg'] else None
        if e and abs(e[0] - s['start'][0]) < .01 and abs(e[1] - s['start'][1]) < .01: s['closed'] = True
    return subs


def flatten(s):
    P = [s['start']]
    for g in s['seg']:
        if g[0] == 'l': P.append(g[1])
        else:
            a, b, c, e = P[-1], g[1], g[2], g[3]
            for k in range(1, 13):
                t = k / 12; u = 1 - t
                P.append(tuple(u**3 * a[i] + 3 * u * u * t * b[i] + 3 * u * t * t * c[i] + t**3 * e[i] for i in (0, 1)))
    return P


def clip_polygon(P, r):
    out = list(P)
    for inside, cross in ((lambda p: p[0] >= r[0], lambda a, b: (r[0], a[1] + (b[1] - a[1]) * (r[0] - a[0]) / (b[0] - a[0]))),
                          (lambda p: p[0] <= r[2], lambda a, b: (r[2], a[1] + (b[1] - a[1]) * (r[2] - a[0]) / (b[0] - a[0]))),
                          (lambda p: p[1] >= r[1], lambda a, b: (a[0] + (b[0] - a[0]) * (r[1] - a[1]) / (b[1] - a[1]), r[1])),
                          (lambda p: p[1] <= r[3], lambda a, b: (a[0] + (b[0] - a[0]) * (r[3] - a[1]) / (b[1] - a[1]), r[3]))):
        src, out = out, []
        for i, p in enumerate(src):
            q = src[i - 1]
            if inside(p):
                if not inside(q): out.append(cross(q, p))
                out.append(p)
            elif inside(q): out.append(cross(q, p))
        if not out: return []
    return out


def clip_polyline(P, r):
    res, cur = [], []
    for a, b in zip(P, P[1:]):
        t0, t1, dx, dy, ok = 0., 1., b[0] - a[0], b[1] - a[1], True
        for p, q in ((-dx, a[0] - r[0]), (dx, r[2] - a[0]), (-dy, a[1] - r[1]), (dy, r[3] - a[1])):
            if p == 0:
                if q < 0: ok = False
            else:
                t = q / p
                if p < 0: t0 = max(t0, t)
                else: t1 = min(t1, t)
        if not ok or t0 > t1:
            if len(cur) > 1: res.append(cur)
            cur = []; continue
        A, B = (a[0] + t0 * dx, a[1] + t0 * dy), (a[0] + t1 * dx, a[1] + t1 * dy)
        if not cur: cur = [A]
        cur.append(B)
        if t1 < 1:
            res.append(cur); cur = []
    if len(cur) > 1: res.append(cur)
    return res


def is_circle(d):
    it = d['items']
    if len(it) not in (4, 8) or any(i[0] != 'c' for i in it): return False
    r = d['rect']; return r.width > 0 and abs(r.width - r.height) < .03 * r.width and r.width < 30


def geometry(subs, fill):
    X = [p[0] for s in subs for g in ([('l', s['start'])] + s['seg']) for p in g[1:]]; Y = [p[1] for s in subs for g in ([('l', s['start'])] + s['seg']) for p in g[1:]]
    x0, y0, x1, y1 = min(X), min(Y), max(X), max(Y); W, H = max(1, emu(x1 - x0)), max(1, emu(y1 - y0))
    pt = lambda p: f'<a:pt x="{emu(p[0] - x0)}" y="{emu(p[1] - y0)}"/>'
    body = ''
    for s in subs:
        body += f'<a:moveTo>{pt(s["start"])}</a:moveTo>'
        for g in s['seg']:
            body += f'<a:lnTo>{pt(g[1])}</a:lnTo>' if g[0] == 'l' else f'<a:cubicBezTo>{pt(g[1])}{pt(g[2])}{pt(g[3])}</a:cubicBezTo>'
        if s['closed']: body += '<a:close/>'
    f = '' if fill else ' fill="none"'
    return x0, y0, W, H, f'<a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/><a:rect l="0" t="0" r="r" b="b"/><a:pathLst><a:path w="{W}" h="{H}"{f}>{body}</a:path></a:pathLst></a:custGeom>'


def sp(i, name, x, y, W, H, geom, fill, ln):
    return parse_xml(f'<p:sp {NS}><p:nvSpPr><p:cNvPr id="{i}" name="{name} {i}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{W}" cy="{H}"/></a:xfrm>{geom}{fill}{ln}</p:spPr></p:sp>')


def connector(i, a, b, ln):
    x, y, W, H = min(a[0], b[0]), min(a[1], b[1]), emu(abs(a[0] - b[0])), emu(abs(a[1] - b[1]))
    fl = (' flipH="1"' if b[0] < a[0] else '') + (' flipV="1"' if b[1] < a[1] else '')
    return parse_xml(f'<p:cxnSp {NS}><p:nvCxnSpPr><p:cNvPr id="{i}" name="line {i}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr><a:xfrm{fl}><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{W}" cy="{H}"/></a:xfrm><a:prstGeom prst="line"><a:avLst/></a:prstGeom>{ln}</p:spPr></p:cxnSp>')


def add_drawing(tree, d, clip, nid):
    r = d['rect']; kind = d['type']; has_fill = 'f' in kind and d.get('fill') is not None; has_stroke = 's' in kind and bool(d.get('width'))
    if not has_fill and not has_stroke: return nid
    fx = fill_xml(d.get('fill') if has_fill else None, d.get('fill_opacity')); lx = line_xml(d) if has_stroke else '<a:ln><a:noFill/></a:ln>'
    subs = subpaths(d)
    if not subs: return nid
    if clip is not None and (r.x0 < clip[0] - .05 or r.y0 < clip[1] - .05 or r.x1 > clip[2] + .05 or r.y1 > clip[3] + .05):
        out = []
        for s in subs:
            P = flatten(s)
            if has_fill or s['closed']:
                Q = clip_polygon(P, clip)
                if len(Q) > 2: out.append(dict(start=Q[0], seg=[('l', p) for p in Q[1:]], closed=True))
            else:
                out += [dict(start=c[0], seg=[('l', p) for p in c[1:]], closed=False) for c in clip_polyline(P, clip)]
        subs = out
        if not subs: return nid
    elif len(d['items']) == 1 and d['items'][0][0] == 'l' and has_stroke:
        a, b = tuple(d['items'][0][1]), tuple(d['items'][0][2])
        tree.append(connector(nid, a, b, lx)); return nid + 1
    if is_circle(d) and clip is None or (is_circle(d) and r.x0 >= clip[0] and r.x1 <= clip[2] and r.y0 >= clip[1] and r.y1 <= clip[3]):
        tree.append(sp(nid, 'marker', r.x0, r.y0, max(1, emu(r.width)), max(1, emu(r.height)), '<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>', fx, lx)); return nid + 1
    x, y, W, H, g = geometry(subs, has_fill)
    name = 'area' if has_fill and r.width > 12 else ('marker' if has_fill else 'curve')
    tree.append(sp(nid, name, x, y, W, H, g, fx, lx)); return nid + 1


def font(n):
    if 'DejaVu' in n or 'Arial' in n or 'Helvet' in n: return 'Arial'
    return 'Times New Roman'


def add_text(tree, line, nid):
    S = [s for s in line['spans'] if s['text'].strip()]
    if not S: return nid
    runs, prev = '', None; horiz = abs(line['dir'][0]) >= abs(line['dir'][1])
    for s in S:
        if prev is not None:
            gap = (s['bbox'][0] - prev['bbox'][2]) if horiz else (prev['bbox'][1] - s['bbox'][3])
            if gap > .18 * s['size'] and not prev['text'].endswith(' ') and not s['text'].startswith(' '): s = dict(s, text=' ' + s['text'])
        n = s['font']; b = 1 if 'Bold' in n else 0; it = 1 if ('Italic' in n or 'Oblique' in n) else 0; c = '%06X' % s['color']
        runs += f'<a:r><a:rPr lang="en-US" sz="{max(100, int(round(s["size"] * 100)))}" b="{b}" i="{it}" dirty="0"><a:solidFill><a:srgbClr val="{c}"/></a:solidFill><a:latin typeface="{font(n)}"/><a:ea typeface="{font(n)}"/><a:cs typeface="{font(n)}"/></a:rPr><a:t>{escape(s["text"])}</a:t></a:r>'
        prev = s
    size = max(s['size'] for s in S); o = S[0]['origin']; H = 1.25 * size
    b0 = [s['bbox'] for s in S]
    ang = math.degrees(math.atan2(line['dir'][1], line['dir'][0])); rot = 0; vert = ''
    bw, bh = max(b[2] for b in b0) - min(b[0] for b in b0), max(b[3] for b in b0) - min(b[1] for b in b0)
    if abs(ang) < 1:
        W = bw + 2; left, top, cx_, cy_ = o[0], o[1] - ASC * size, W, H
    elif abs(ang + 90) < 1:   # running upward: PowerPoint's "rotate all text 270", the box itself is not rotated
        W = bh + 2; left, top, cx_, cy_, vert = o[0] - ASC * size, o[1] - W, H, W, ' vert="vert270"'
    else:                     # any other angle: a rotated text box
        a = math.radians(ang); W = max(bw / max(abs(math.cos(a)), .2), 1.) + 2; off = ASC * size - H / 2
        cx = o[0] + W / 2 * math.cos(a) + off * math.sin(a); cy = o[1] + W / 2 * math.sin(a) - off * math.cos(a)
        left, top, cx_, cy_ = cx - W / 2, cy - H / 2, W, H; rot = int(round((ang % 360) * 60000))
    tree.append(parse_xml(f'<p:sp {NS}><p:nvSpPr><p:cNvPr id="{nid}" name="text {nid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm rot="{rot}"><a:off x="{emu(left)}" y="{emu(top)}"/><a:ext cx="{emu(cx_)}" cy="{emu(cy_)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr{vert} wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:noAutofit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="l"/>{runs}</a:p></p:txBody></p:sp>'))
    return nid + 1


def convert(src, dst):
    doc = pymupdf.open(src); page = doc[0]; rect = page.rect
    prs = Presentation(); prs.slide_width = Emu(emu(rect.width)); prs.slide_height = Emu(emu(rect.height))
    slide = prs.slides.add_slide(prs.slide_layouts[6]); tree = slide.shapes._spTree; nid = 2
    infos = page.get_image_info(xrefs=True)
    def place(m):
        nonlocal nid
        x = m['xref']; pix = pymupdf.Pixmap(doc, x); sm = doc.extract_image(x).get('smask', 0)
        if pix.colorspace is not None and pix.colorspace.n > 3: pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        if sm: pix = pymupdf.Pixmap(pix, pymupdf.Pixmap(doc, sm))
        b = m['bbox']; pic = slide.shapes.add_picture(io.BytesIO(pix.tobytes('png')), Emu(emu(b[0])), Emu(emu(b[1])), Emu(emu(b[2] - b[0])), Emu(emu(b[3] - b[1])))
        pic._element.nvPicPr.cNvPr.set('id', str(nid)); pic._element.nvPicPr.cNvPr.set('name', f'map {nid}'); nid += 1
    # Layers: backgrounds that lie under a map, then all maps, then lines, markers and areas in PDF order, then text.
    # (The PDF's own order cannot be recovered reliably, and in these figures nothing vector lies under a map but its background.)
    drawings = page.get_drawings(extended=True)
    under = lambda d: d['type'] in ('f', 'fs') and any(d['rect'].x0 <= i['bbox'][0] + 1 and d['rect'].y0 <= i['bbox'][1] + 1 and d['rect'].x1 >= i['bbox'][2] - 1 and d['rect'].y1 >= i['bbox'][3] - 1 for i in infos)
    white = lambda d: d['type'] == 'f' and d.get('fill') == (1.0, 1.0, 1.0) and d['rect'].width * d['rect'].height > 1000
    for phase in ('under', 'maps', 'over'):
        if phase == 'maps':
            for m in infos: place(m)
            continue
        stack = []
        for d in drawings:
            lv = d.get('level', 0); stack = [s for s in stack if s[0] < lv]
            if d['type'] == 'clip': stack.append((lv, tuple(d['scissor']))); continue
            if d['type'] == 'group' or white(d) or under(d) != (phase == 'under'): continue
            clip = None
            if stack:
                clip = (max(s[1][0] for s in stack), max(s[1][1] for s in stack), min(s[1][2] for s in stack), min(s[1][3] for s in stack))
            nid = add_drawing(tree, d, clip, nid)
    for b in page.get_text('dict')['blocks']:
        if b['type'] == 0:
            for l in b['lines']: nid = add_text(tree, l, nid)
    Path(dst).parent.mkdir(parents=True, exist_ok=True); prs.save(dst)
    return nid - 2


if __name__ == '__main__':
    if len(sys.argv) > 3: PATTERN = tuple(sys.argv[3].split(','))
    print(sys.argv[2], convert(sys.argv[1], sys.argv[2]), 'objects')
