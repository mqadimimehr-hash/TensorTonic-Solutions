#!/bin/bash
# Refresh SUBMISSION_PACKAGE/ from the current sources (run tools_rebuild.sh first).
# The journal copies of the manuscript and SI are built WITHOUT the internal "Revision note"
# blockquotes; the working copies in manuscript_v4/ and supporting_information_v4/ keep them.
set -e
R=/home/user/TensorTonic-Solutions/DFT_paper_revision
P=$R/SUBMISSION_PACKAGE
S=/tmp/claude-0/-home-user-TensorTonic-Solutions/0159629d-9bba-513e-9e05-92ed56279e63/scratchpad/package; mkdir -p $S
CH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
strip_note() {  # drop the blockquote paragraph that starts with "> **Revision note"
  python3 - "$1" "$2" <<'PY'
import sys
lines = open(sys.argv[1]).read().split("\n")
i = next(k for k, l in enumerate(lines) if l.startswith("> **Revision note"))
j = i
while j < len(lines) and lines[j].strip():   # the note runs to the next blank line
    j += 1
out = "\n".join(lines[:i] + lines[j + 1:])
assert "Revision note" not in out
open(sys.argv[2], "w").write(out)
PY
}
strip_note $R/manuscript_v4/Ghadimimehr_DFT_TiO2_PrRb_v4_MANUSCRIPT.md $S/ms.md
strip_note $R/supporting_information_v4/SI_v4.md $S/si.md
cd $R/manuscript_v4 && pandoc $S/ms.md --resource-path=.:.. -o $P/02_Manuscript.docx
pandoc $S/ms.md --resource-path=.:.. -s --metadata title=" " --embed-resources -o $S/ms.html
cd $R/supporting_information_v4 && pandoc $S/si.md --resource-path=.:.. -o $P/06_Supporting_Information.docx
pandoc $S/si.md --resource-path=.:.. -s --metadata title=" " --embed-resources -o $S/si.html
python3 - <<PY
css='<style>body{font-family:"DejaVu Serif",serif;font-size:10.5pt;max-width:17cm;margin:1.2cm auto;line-height:1.35} table{border-collapse:collapse;font-size:8pt;margin:8px 0} th,td{border:1px solid #999;padding:2px 5px} img{max-width:100%;height:auto} h1{font-size:15pt}</style></head>'
for n in ['ms','si']:
    p='$S/'+n+'.html'; s=open(p).read().replace('</head>',css,1); open(p,'w').write(s)
PY
timeout 120 $CH --headless --no-sandbox --disable-gpu --print-to-pdf=$P/02_Manuscript_preview.pdf --no-pdf-header-footer file://$S/ms.html >/dev/null 2>&1
timeout 120 $CH --headless --no-sandbox --disable-gpu --print-to-pdf=$P/06_Supporting_Information_preview.pdf --no-pdf-header-footer file://$S/si.html >/dev/null 2>&1
# cover letter, highlights, graphical abstract, figures
cp $R/submission/Cover_Letter_Applied_Surface_Science.docx $P/01_Cover_Letter.docx
sed '1s/^# Highlights.*/# Highlights/' $R/submission/Highlights.md | pandoc -f markdown -o $P/03_Highlights.docx
cp $R/figures/Graphical_Abstract.png $P/04_Graphical_Abstract.png; cp $R/figures/Graphical_Abstract.pdf $P/04_Graphical_Abstract.pdf
for i in 1 2 3 4; do
  src=$(ls $R/figures/Fig${i}_*_v4.pdf); cp $src $P/05_Figures/Figure_$i.pdf; cp ${src%.pdf}.png $P/05_Figures/Figure_$i.png
done
# Zenodo folder: scripts expect their data in ./data (as in figures/)
Z=$P/07_Data_and_scripts_for_Zenodo
rm -rf $Z/figure_data; mkdir -p $Z/data
cp $R/figures/data/PDOS_*.csv $R/figures/data/lowdin_*.csv $R/figures/data/nscf_Rb_VO.out $Z/data/
cp $R/figures/{make_figures,make_pdos_figures,make_fig1_structures,make_graphical_abstract,extract_lowdin}.py $Z/
cp $R/supporting_information_v4/{energy_ledger.csv,check_ledger.py} $Z/
# checks
for f in $P/02_Manuscript.docx $P/06_Supporting_Information.docx; do
  n=$(unzip -p $f word/document.xml | grep -o "Revision note" | wc -l); echo "$(basename $f): revision notes left = $n"
done
(cd $Z && python3 check_ledger.py | tail -1 && python3 -c "import ast,sys; [ast.parse(open(f).read()) for f in ['make_pdos_figures.py','make_fig1_structures.py']]" && echo "Zenodo scripts parse")
cd $R && rm -f SUBMISSION_PACKAGE.zip && zip -qr SUBMISSION_PACKAGE.zip SUBMISSION_PACKAGE && echo "zip: $(du -h SUBMISSION_PACKAGE.zip | cut -f1)"
