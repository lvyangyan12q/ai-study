import os, re, shutil, json
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
LS = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687921332_2e58013d1c/learning-space")
SRC = os.path.join(LS, "sources")
# rename
a = os.path.join(SRC, "12-factor-agents"); b = os.path.join(SRC, "12-factor-agents-main")
if os.path.isdir(a) and not os.listdir(a): shutil.rmtree(a, ignore_errors=True)
if os.path.isdir(b) and not os.path.isdir(a): os.rename(b, a)
print("sources:", os.listdir(SRC))

R = os.path.join(SRC, "ai-agent-book")
learn = open(os.path.join(R,"docs/zh-CN/LEARNING.md"), encoding="utf-8").read()
print("LEARNING chars:", len(learn))
print("---- LEARNING tail ----")
print(learn[2600:])

# 解析实验状态表
st = open(os.path.join(R,"docs/EXPERIMENT_STATUS.md"), encoding="utf-8", errors="ignore").read()
print("---- EXPERIMENT_STATUS chars:", len(st))
rows = re.findall(r"^\|\s*(\d+)-(\d+)\s*\|([^|]*)\|([^|]*)\|", st, re.M)
from collections import Counter, defaultdict
cnt = defaultdict(Counter)
for ch, num, kind, verdict in rows:
    v = verdict.strip()
    k = "Complete" if v.startswith("**Complete") else ("Incomplete" if "Incomplete" in v else ("Partial" if v.startswith("**Partial") else "Other"))
    cnt[int(ch)][k] += 1
print("按章实验统计（行数仅统计正文中的表格行）:", {k: dict(v) for k,v in sorted(cnt.items())})
print("总行数:", len(rows))