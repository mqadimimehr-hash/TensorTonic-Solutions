#!/bin/bash
# Rebuild manuscript v4 and SI v4 Word files, validate them, and refresh the Chromium previews.
set -e
R=/home/user/TensorTonic-Solutions/DFT_paper_revision
S=/tmp/claude-0/-home-user-TensorTonic-Solutions/0159629d-9bba-513e-9e05-92ed56279e63/scratchpad/render; mkdir -p $S
V=/root/.claude/skills/synced/2168826f-d55a-4089-9c1e-c0ca1653b3e5_a44c79bc-00c2-4bd3-890f-bb755421f61a/docx/scripts/office/validate.py
CH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
cd $R/manuscript_v4
cat part1_front_intro_methods.md part2_results.md part3_discussion_end.md > manuscript_v4_src.md
python3 build_refs.py manuscript_v4_src.md Ghadimimehr_DFT_TiO2_PrRb_v4_MANUSCRIPT.md
pandoc Ghadimimehr_DFT_TiO2_PrRb_v4_MANUSCRIPT.md --resource-path=.:.. -o Ghadimimehr_DFT_TiO2_PrRb_v4_MANUSCRIPT.docx
pandoc Ghadimimehr_DFT_TiO2_PrRb_v4_MANUSCRIPT.md --resource-path=.:.. -s --metadata title=" " --embed-resources -o $S/ms.html
cd $R/supporting_information_v4
pandoc SI_v4.md --resource-path=.:.. -o Ghadimimehr_DFT_TiO2_PrRb_v4_Supporting_Information.docx
pandoc SI_v4.md --resource-path=.:.. -s --metadata title=" " --embed-resources -o $S/si.html
python3 - <<PY
css='<style>body{font-family:"DejaVu Serif",serif;font-size:10.5pt;max-width:17cm;margin:1.2cm auto;line-height:1.35} table{border-collapse:collapse;font-size:8pt;margin:8px 0} th,td{border:1px solid #999;padding:2px 5px} img{max-width:100%;height:auto} h1{font-size:15pt}</style></head>'
for n in ['ms','si']:
    p='$S/'+n+'.html'; s=open(p).read().replace('</head>',css,1); open(p,'w').write(s)
PY
for n in ms si; do timeout 120 $CH --headless --no-sandbox --disable-gpu --print-to-pdf=$S/$n.pdf --no-pdf-header-footer file://$S/$n.html >/dev/null 2>&1; done
cp $S/ms.pdf $R/manuscript_v4/Ghadimimehr_DFT_TiO2_PrRb_v4_MANUSCRIPT_PREVIEW.pdf
cp $S/si.pdf $R/supporting_information_v4/Ghadimimehr_DFT_TiO2_PrRb_v4_Supporting_Information_PREVIEW.pdf
for f in $R/manuscript_v4/Ghadimimehr_DFT_TiO2_PrRb_v4_MANUSCRIPT.docx $R/supporting_information_v4/Ghadimimehr_DFT_TiO2_PrRb_v4_Supporting_Information.docx; do echo "== $(basename $f)"; python3 $V "$f" 2>&1 | tail -1; done
grep -c "{{" $R/manuscript_v4/Ghadimimehr_DFT_TiO2_PrRb_v4_MANUSCRIPT.md || true
echo "words: $(wc -w < $R/manuscript_v4/Ghadimimehr_DFT_TiO2_PrRb_v4_MANUSCRIPT.md)"
echo "abstract words: $(awk '/^\*\*Abstract\*\*/{f=1;next} /^\*\*Keywords/{f=0} f' $R/manuscript_v4/part1_front_intro_methods.md | wc -w)"
