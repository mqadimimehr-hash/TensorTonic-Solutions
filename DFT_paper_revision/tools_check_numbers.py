"""Compare numeric tokens between backup (.bak) and edited sources; report any number removed or introduced."""
import re, sys, collections
pairs = [("manuscript_v4/part1.bak","manuscript_v4/part1_front_intro_methods.md"),
         ("manuscript_v4/part2.bak","manuscript_v4/part2_results.md"),
         ("manuscript_v4/part3.bak","manuscript_v4/part3_discussion_end.md"),
         ("supporting_information_v4/SI_v4.bak","supporting_information_v4/SI_v4.md")]
num = re.compile(r'(?<![A-Za-z_])[−\-+]?\d+(?:[.,]\d+)*(?:×10\^?[−\-]?\d+\^?)?')
ok = True
for bak, cur in pairs:
    a = collections.Counter(num.findall(open(bak).read()))
    b = collections.Counter(num.findall(open(cur).read()))
    removed = {k: v for k, v in (a - b).items()}
    added = {k: v for k, v in (b - a).items()}
    print(f"== {cur}: removed {sum(removed.values())} token(s), added {sum(added.values())} token(s)")
    if removed: print("   removed:", dict(sorted(removed.items())))
    if added: print("   added:  ", dict(sorted(added.items())))
    if removed or added: ok = False
print("NUMERIC CONTENT UNCHANGED" if ok else "REVIEW THE NUMERIC CHANGES ABOVE (section renumbering or ref numbers may explain some)")
