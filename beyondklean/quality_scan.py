"""Flag task content that is too thin for publication."""
import importlib.util, sys
from pathlib import Path
C = {}
for p in sorted(Path("content").glob("f[0-9][0-9]*.py")):
    s = importlib.util.spec_from_file_location(p.stem, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    for k, v in m.C.items(): C[k] = (p.stem, v)
for p in sorted(Path("content").glob("p[0-9][0-9]*.py")):
    s = importlib.util.spec_from_file_location(p.stem, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    for k, v in m.P.items(): C[k] = (C[k][0], {**C[k][1], **v})
wc = lambda t: len(t.split())
thin = []
for k, (f, c) in C.items():
    short_ans = sum(1 for q, a in c["q"] if wc(a) < 12 or wc(q) < 5)
    problems = []
    if short_ans: problems.append(f"{short_ans} short answers")
    if wc(c["a"]) < 20: problems.append("short lede")
    if wc(c["y"]) < 15: problems.append("short why")
    if wc(c["m"]) < 12: problems.append("short method")
    if any(wc(x) < 5 for x in c["w"]): problems.append("terse lists")
    if problems: thin.append((f, k, problems))
print(len(thin), "of", len(C), "need work")
if "-v" in sys.argv:
    for f, k, p in thin: print(f, "|", k, "|", ", ".join(p))
