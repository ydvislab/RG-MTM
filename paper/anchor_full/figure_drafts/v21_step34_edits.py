"""v21 steps 3-4: new abstract, introduction paragraph, related work, evaluation, discussion and conclusion.
Each replaced span is located by unique markers and checked for size before it is replaced."""
from pathlib import Path
H = Path(__file__).resolve().parent; T = H / 'v21_text'; D = H.parents[1] / 'pvis2027/latex_v21'
s = (D / 'main.tex').read_text(); n0 = len(s)


def span(start, end, maxlen, keep_end=True):
    global s
    i = s.index(start); j = s.index(end, i)
    assert s.count(start) == 1 and j - i <= maxlen, (start[:40], j - i)
    return i, j


def put(start, end, new, maxlen):
    global s
    i, j = span(start, end, maxlen); s = s[:i] + new + s[j:]


put('\\abstract{', '\\keywords{', (T / 'abstract.tex').read_text(), 2600)
put('We answer these questions.', 'Our main contributions are as follows:', (T / 'intro_p4.tex').read_text(), 1500)
s = s.replace('% Former Figure 2 temporarily removed; source retained in figures/source/ring_result_20261106.\n', '')
put('\\section{Related Work}\\label{sec:related}', '\\section{Spatially Anchored Merge Tree Maps}', (T / 'related.tex').read_text(), 6000)
put('\\section{Experiments}\\label{sec:experiments}', '\\section{Discussion and Limitations}', (T / 'evaluation.tex').read_text(), 20000)
put('\\section{Discussion and Limitations}', '% Flush pending floats', (T / 'discussion.tex').read_text(), 4000)
(D / 'main.tex').write_text(s)
print('main.tex', n0, '->', len(s))
