#!/bin/bash
# Build main.pdf and supplementary.pdf from a scratch copy of latex_v30 with pdflatex.
# The cm-super map is loaded on the command line so that the sans fonts are embedded as Type 1 (the source is untouched).
set -e
SRC="C:/Users/ASUS/Desktop/RG-MTM/paper/pvis2027/latex_v30"
B="C:/Users/ASUS/AppData/Local/Temp/claude/dc8d4bc441ce0d46/33aac687-2417-4db3-a17a-436fbacc9efb/scratchpad/build"
rm -rf "$B"; mkdir -p "$B"; cp -r "$SRC/." "$B/"; cd "$B"
for doc in main supplementary; do
  run() { pdflatex -interaction=nonstopmode -jobname=$doc "\pdfmapfile{+cm-super-t1.map}\input{$doc}" > /dev/null 2>&1 || true; }
  run; bibtex $doc > /dev/null 2>&1 || true; run; run
  echo "== $doc: $(grep -o 'Output written.*' $doc.log)"
  grep -E "^!|Warning: (Reference|Citation)|There were undefined" $doc.log | sort | uniq -c | head || true
  echo "   Type 3 fonts: $(pdffonts $doc.pdf | grep -c 'Type 3' || true)"
done
