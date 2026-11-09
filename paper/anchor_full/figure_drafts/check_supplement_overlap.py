"""Report every run of >= N consecutive words that the supplement shares with the paper (text extracted from the PDFs)."""
import re, subprocess, sys
B = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 6


def words(pdf, last=None):
    args = ['pdftotext'] + (['-l', str(last)] if last else []) + [pdf, '-']
    t = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
    t = t.split('References')[0] if 'References' in t else t      # bibliography is shared by design
    t = re.sub(r'-\n', '', t)
    return re.findall(r"[a-z0-9]+", t.lower())


main = words(f'{B}/main.pdf'); sup = words(f'{B}/supplementary.pdf')
grams = {tuple(main[i:i + N]) for i in range(len(main) - N + 1)}
hits = [i for i in range(len(sup) - N + 1) if tuple(sup[i:i + N]) in grams]
runs, cur = [], None
for i in hits:
    if cur and i <= cur[1] + 1: cur[1] = i
    else:
        cur = [i, i]; runs.append(cur)
print(f'{len(runs)} shared runs of >= {N} words')
for a, b in runs: print('  -', ' '.join(sup[a:b + N]))
