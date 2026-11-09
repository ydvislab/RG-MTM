"""Convert main_zh.tex (v24) to main_zh.md, reusing the hand-made Markdown tables of the previous main_zh.md.

Usage: python tex2md_zh.py <latex_v21 dir> <aux file>
Numbers for \\ref and \\cite come from the compiled aux file, so they match the PDFs.
"""
import io, re, sys
from pathlib import Path

D = Path(sys.argv[1]); AUX = Path(sys.argv[2])
BS = chr(92)
tex = io.open(D / 'main_zh.tex', encoding='utf-8').read()
old_md = io.open(D / 'main_zh.md', encoding='utf-8').read().splitlines()
aux = io.open(AUX, encoding='utf-8').read()

labels = {}
for m in re.finditer(re.escape(BS + 'newlabel{') + r'([^}@]+)\}\{\{([^}]*)\}', aux):
    labels[m.group(1)] = m.group(2)
bib = dict(re.findall(re.escape(BS + 'bibcite{') + r'([^}]+)\}\{(\d+)\}', aux))


def old_table(k):
    start = next(i for i, l in enumerate(old_md) if l.startswith(f'**表 {k}**'))
    out = [old_md[start]]; i = start + 1
    while i < len(old_md) and (old_md[i].strip() == '' or old_md[i].startswith('|')):
        out.append(old_md[i]); i += 1
    if i < len(old_md) and old_md[i].startswith(('†', '全部为本地测量')):
        out.append(old_md[i])
    while out and out[-1].strip() == '':
        out.pop()
    return '\n'.join(out)


TABLE_NUM = {'table_family': 1, 'table1_comparison': 2, 'table_data': 3, 'table_volume': 4}


def refs(s):
    s = re.sub(re.escape(BS) + r'ref\{([^}]*)\}', lambda m: labels.get(m.group(1), '??'), s)
    def cite(m):
        nums = sorted(int(bib[k.strip()]) for k in m.group(1).split(','))
        return '[' + ', '.join(map(str, nums)) + ']'
    s = re.sub(r'~?' + re.escape(BS) + r'cite\{([^}]*)\}', cite, s)
    return s


def inline(s):
    s = refs(s)
    s = s.replace('式~(', '式 (').replace('~', ' ')
    s = re.sub(re.escape(BS) + r'emph\{([^}]*)\}', r'**\1**', s)
    s = re.sub(re.escape(BS) + r'textbf\{([^}]*)\}', r'**\1**', s)
    s = s.replace('$' + BS + 'mu$g/m$^3$', 'μg/m³').replace(BS + ',μg', ' μg')
    parts = s.split('$')
    for k in range(0, len(parts), 2):
        parts[k] = parts[k].replace(BS + '%', '%').replace(BS + ',', ' ').replace('--', '–')
    s = '$'.join(parts)
    s = s.replace('Hovm' + BS + '"oller', 'Hovmöller')
    s = s.replace('PM$_{2.5}$', 'PM₂.₅').replace(BS + 'mu$g/m$^3$', 'μg/m³').replace('$' + BS + 'mu$g/m$^3$', 'μg/m³')
    s = s.replace(BS + 'dtop', 'd_{\\mathrm{top}}').replace(BS + 'nroe', '\\mathrm{NROE}').replace(BS + 'lca', '\\operatorname{lca}')
    s = s.replace('$^' + BS + 'circ$', '°')
    return s


def block_math(env_body, label):
    body = env_body.strip()
    body = body.replace(BS + 'dtop', 'd_{\\mathrm{top}}').replace(BS + 'nroe', '\\mathrm{NROE}').replace(BS + 'lca', '\\operatorname{lca}')
    tag = f' \\tag{{{labels[label]}}}' if label in labels else ''
    return f'$$\n{body}{tag}\n$$'


def caption_of(fig):
    m = re.search(re.escape(BS + 'caption{') + r'(.*)\}\s*' + re.escape(BS + 'label{') + r'([^}]*)\}', fig, re.S)
    return m.group(1), m.group(2)


# ---- header pieces (teaser caption, abstract, keywords) ----
teaser = re.search(r'图~' + re.escape(BS + 'thefigure') + r'：(.*?)' + re.escape(BS + 'par}'), tex, re.S).group(1)
abstract = re.search(re.escape(BS + 'abstract{') + r'(.*?)\}\n' + re.escape(BS + 'keywords'), tex, re.S).group(1)
keywords = re.search(re.escape(BS + 'keywords{') + r'(.*?)\}\n', tex).group(1)

out = []
out.append('# AnchorMTM：带位置下界的空间锚定合并树地图\n')
out.append('**中文译稿（正式稿，与 `main.tex` v25 逐句对应，2026-11-09）**\n')
out.append('Lele Wang¹²\\*　Yu Dong¹\\*　Yuxiang Meng¹²　Guan Li¹²　Zhe Wang¹²　Guihua Shan¹²³　Jun Liu¹²†\n')
out.append('¹ 中国科学院计算机网络信息中心先进交互式技术与应用研究室，北京  \n² 中国科学院大学，北京  \n³ 国科大杭州高等研究院，杭州\n')
out.append('\\* Lele Wang 与 Yu Dong 对本文贡献相同。　† 通讯作者，liujun@sccas.cn。  \n邮箱：lelewang@cnic.cn；dongyu@cnic.cn；yxmeng@cnic.cn；liguan@sccas.cn；wangzhe@sccas.cn；shanghuihua@sccas.cn；liujun@sccas.cn\n')
out.append('> 译稿说明：由 `main_zh.tex` 自动转换；公式保留原文写法；图、表、节、定理、式和参考文献编号与英文 PDF 一致。排版以 `paper/1037_v25_zh.pdf` 为准。\n')
out.append('---\n')
out.append('**图 1** ' + inline(teaser.strip()) + '\n')
out.append('## 摘要\n')
out.append(inline(abstract.strip()) + '\n')
out.append('**关键词：** ' + keywords + '\n')

body = tex.split(BS + 'begin{document}', 1)[1].split(BS + 'FloatBarrier', 1)[0]
body = re.sub(r'(?m)^%.*\n', '', body)
for cmd in ('maketitle', 'raggedbottom'):
    body = body.replace(BS + cmd, '')
body = re.sub(re.escape(BS + 'setlength{') + r'[^}]*\}\{[^}]*\}', '', body)

sec = 0; sub = 0
tokens = re.split(r'(' + re.escape(BS) + r'begin\{figure\*?\}.*?' + re.escape(BS) + r'end\{figure\*?\}'
                  r'|' + re.escape(BS) + r'begin\{equation\}.*?' + re.escape(BS) + r'end\{equation\}'
                  r'|' + re.escape(BS) + r'begin\{theorem\}.*?' + re.escape(BS) + r'end\{theorem\}'
                  r'|' + re.escape(BS) + r'begin\{proposition\}.*?' + re.escape(BS) + r'end\{proposition\}'
                  r'|' + re.escape(BS) + r'begin\{proof\}.*?' + re.escape(BS) + r'end\{proof\}'
                  r'|' + re.escape(BS) + r'begin\{itemize\}.*?' + re.escape(BS) + r'end\{itemize\})', body, flags=re.S)
pending = []


def emit_text(t):
    global sec, sub
    for para in re.split(r'\n\s*\n', t):
        lines = []
        for line in para.split('\n'):
            m = re.match(re.escape(BS) + r'(firstsection|section)\{([^}]*)\}', line.strip())
            if m:
                sec += 1; sub = 0; out.append(f'## {sec} {m.group(2)}\n'); continue
            m = re.match(re.escape(BS) + r'subsection\{([^}]*)\}', line.strip())
            if m:
                sub += 1; out.append(f'### {sec}.{sub} {m.group(1)}\n'); continue
            m = re.match(re.escape(BS) + r'input\{tables_zh/([^}.]*)\.tex\}', line.strip())
            if m:
                out.append(old_table(TABLE_NUM[m.group(1)]) + '\n'); continue
            lines.append(line)
        text = ' '.join(l.strip() for l in lines).strip()
        text = re.sub(re.escape(BS) + r'label\{[^}]*\}', '', text).strip()
        text = re.sub(re.escape(BS) + r'paragraph\{([^}]*)\}\s*', r'**\1** ', text)
        if text:
            out.append(inline(text) + '\n')
            while pending:
                out.append(pending.pop(0) + '\n')


for tok in tokens:
    if tok.startswith(BS + 'begin{figure'):
        cap, lab = caption_of(tok)
        out.append(f'**图 {labels[lab]}** ' + inline(cap) + '\n')
    elif tok.startswith(BS + 'begin{equation}'):
        lab = re.search(re.escape(BS + 'label{') + r'([^}]*)\}', tok).group(1)
        inner = re.sub(re.escape(BS) + r'(begin|end)\{equation\}|' + re.escape(BS) + r'label\{[^}]*\}', '', tok)
        inner = inner.replace(BS + 'begin{split}', BS + 'begin{aligned}').replace(BS + 'end{split}', BS + 'end{aligned}')
        out.append(block_math(inner, lab) + '\n')
    elif tok.startswith((BS + 'begin{theorem}', BS + 'begin{proposition}')):
        kind = 'theorem' if 'theorem' in tok[:20] else 'proposition'
        name = re.match(re.escape(BS) + r'begin\{\w+\}\[([^\]]*)\]', tok).group(1)
        lab = re.search(re.escape(BS + 'label{') + r'([^}]*)\}', tok).group(1)
        inner = re.sub(re.escape(BS) + r'begin\{\w+\}\[[^\]]*\]' + re.escape(BS) + r'label\{[^}]*\}|' + re.escape(BS) + r'end\{(theorem|proposition)\}', '', tok)
        parts = re.split(r'(' + re.escape(BS) + r'begin\{equation\}.*?' + re.escape(BS) + r'end\{equation\})', inner, flags=re.S)
        head = f'**{"定理" if kind == "theorem" else "命题"} {labels[lab]}（{name}）** '
        buf = []
        for p in parts:
            if p.startswith(BS + 'begin{equation}'):
                el = re.search(re.escape(BS + 'label{') + r'([^}]*)\}', p).group(1)
                eq = re.sub(re.escape(BS) + r'(begin|end)\{equation\}|' + re.escape(BS) + r'label\{[^}]*\}', '', p)
                eq = eq.replace(BS + 'begin{split}', BS + 'begin{aligned}').replace(BS + 'end{split}', BS + 'end{aligned}')
                buf.append('\n\n' + block_math(eq, el) + '\n\n')
            else:
                buf.append(inline(' '.join(x.strip() for x in p.strip().split('\n'))))
        out.append(head + ''.join(buf) + '\n')
    elif tok.startswith(BS + 'begin{proof}'):
        inner = re.sub(re.escape(BS) + r'begin\{proof\}\[[^\]]*\]|' + re.escape(BS) + r'end\{proof\}', '', tok)
        out.append('*证明要点。* ' + inline(' '.join(x.strip() for x in inner.strip().split('\n'))) + ' □\n')
    elif tok.startswith(BS + 'begin{itemize}'):
        items = re.split(re.escape(BS) + r'item\s*', tok)[1:]
        for it in items:
            it = re.sub(re.escape(BS) + r'end\{itemize\}', '', it)
            out.append('- ' + inline(' '.join(x.strip() for x in it.strip().split('\n'))))
        out.append('')
    else:
        emit_text(tok)

md = '\n'.join(out).rstrip() + '\n\n## 参考文献\n\n见英文 PDF（编号相同）。\n'
md = re.sub(r'\n{3,}', '\n\n', md)
assert BS + 'ref{' not in md and BS + 'cite{' not in md and '??' not in md, 'unresolved reference'
io.open(D / 'main_zh.md', 'w', encoding='utf-8', newline='\n').write(md)
print('written', len(md), 'chars;', 'sections', sec)
