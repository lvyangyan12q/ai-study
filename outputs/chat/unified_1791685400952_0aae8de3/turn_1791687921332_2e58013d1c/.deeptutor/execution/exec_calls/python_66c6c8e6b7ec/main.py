import os, re, json
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687921332_2e58013d1c")
BOOK = os.path.join(NEW, "learning-space/sources/ai-agent-book/book")

out = {}
for i in list(range(1,11)):
    fp = os.path.join(BOOK, f"chapter{i}.md")
    if not os.path.exists(fp): continue
    txt = open(fp, encoding="utf-8", errors="ignore").read()
    lines = txt.split("\n")
    h1 = [l for l in lines if re.match(r"^#\s", l)]
    h2 = [l for l in lines if re.match(r"^##\s", l)]
    h3 = [l for l in lines if re.match(r"^###\s", l)]
    out[i] = {
        "title": h1[0].lstrip("# ").strip() if h1 else "(未找到)",
        "h2": [x.lstrip("# ").strip() for x in h2],
        "h3_count": len(h3),
        "chars": len(txt),
        "h3_sample": [x.lstrip("# ").strip() for x in h3[:6]],
    }
print(json.dumps(out, ensure_ascii=False, indent=1)[:6000])