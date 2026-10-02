"""Replace {{key}} citation placeholders with numbers in order of first appearance and append the reference list."""
import re, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from refs import REFS
src = open(sys.argv[1], encoding='utf-8').read()
order, missing = [], []
def num(key):
    if key not in REFS:
        missing.append(key); return f"[??{key}]"
    if key not in order: order.append(key)
    return str(order.index(key) + 1)
def repl(m):
    keys = [k.strip() for k in m.group(1).split(',')]
    nums = [num(k) for k in keys]
    return "[" + ",".join(nums) + "]"
out = re.sub(r"\{\{([^}]+)\}\}", repl, src)
out += "\n\n**References**\n\n" + "\n\n".join(f"({i+1}) {REFS[k]}" for i, k in enumerate(order)) + "\n"
open(sys.argv[2], 'w', encoding='utf-8').write(out)
unused = [k for k in REFS if k not in order]
print(f"{len(order)} references cited; missing keys: {missing}; unused DB entries: {unused}")
