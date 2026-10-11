import os, subprocess, glob
from collections import Counter
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791696096980_527b333145")
R = os.path.join(NEW, "learning-space/sources/ai-agent-book")

for l in glob.glob(os.path.join(R,".git","**","*.lock"), recursive=True):
    try: os.remove(l); print("清锁:", os.path.basename(l))
    except Exception as e: print("清锁失败:", e)

CODE = {".py",".toml",".txt",".yaml",".yml",".sh",".sql",".ts",".js",".json",".cfg",".ini",".dockerfile",".env"}
def ls(ch):
    r = subprocess.run(["git","ls-tree","-r","--name-only","HEAD",ch+"/"], cwd=R,
                       capture_output=True, text=True, timeout=120)
    return [x for x in r.stdout.split("\n") if x.strip()]

tot = Counter(); code_total = 0; grand = 0
for i in range(2, 11):
    ch = f"chapter{i}"
    files = ls(ch)
    ext = Counter(os.path.splitext(f)[1].lower() for f in files)
    code = [f for f in files if os.path.splitext(f)[1].lower() in CODE and "/runs/" not in f]
    md = [f for f in files if f.endswith(".md") and f.count("/") <= 2 and "language" not in f]
    tot.update(ext); grand += len(files); code_total += len(code)
    print(f"{ch}: 总 {len(files)} | 代码类 {len(code)} | 顶层md {len(md)} | 主要扩展名 {ext.most_common(6)}")
print("合计文件:", grand, "其中代码类:", code_total)
print("扩展名总览:", tot.most_common(12))