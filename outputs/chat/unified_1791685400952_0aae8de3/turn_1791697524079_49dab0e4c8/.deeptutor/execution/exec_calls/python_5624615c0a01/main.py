import os, subprocess, fnmatch, time
from collections import Counter
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
LS  = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791697524079_49dab0e4c8/learning-space")
R   = os.path.join(LS, "sources/ai-agent-book"); G = os.path.join(R,".git")

keep = ["/README.md","/README.en.md","/LICENSE","/mkdocs.yml","/pyproject.toml","/.gitignore",
        "/book/","/docs/","/skills/"] + [f"/chapter{i}/" for i in range(1,11)]
drop = [f"!/**/*.{e}" for e in ["mp4","mov","avi","webm","png","jpg","jpeg","gif","webp","pdf","pptx",
        "gz","zip","tar","mp3","wav","m4a","jsonl","ndjson","csv","log","parquet","db","sqlite","sqlite3"]]
drop += [f"!/**/{d}/" for d in ["runs","outputs","traces","checkpoints","__pycache__",".ipynb_checkpoints"]]
drop += ["!/chapter10/book-translation/validation/"]
open(os.path.join(G,"info","sparse-checkout"),"w",encoding="utf-8").write("\n".join(keep+drop)+"\n")

env = dict(os.environ); env["HTTPS_PROXY"] = env["HTTP_PROXY"] = "http://127.0.0.1:7897"
t0=time.time()
r = subprocess.run(["git","-c","core.longpaths=true","-c","http.version=HTTP/1.1",
                    "-c","http.proxy=http://127.0.0.1:7897","sparse-checkout","reapply"],
                   cwd=R, env=env, capture_output=True, text=True, timeout=170)
print("reapply 退出码:", r.returncode, "耗时 %.0f s" % (time.time()-t0))
print("stderr 尾部:", (r.stderr or "").strip()[-400:] or "(无)")

# 完整性核对：期望集合 vs 磁盘
exp = subprocess.run(["git","ls-tree","-r","--name-only","HEAD"],cwd=R,capture_output=True,text=True).stdout.splitlines()
BAD_EXT = {"mp4","mov","avi","webm","png","jpg","jpeg","gif","webp","pdf","pptx","gz","zip","tar",
           "mp3","wav","m4a","jsonl","ndjson","csv","log","parquet","db","sqlite","sqlite3"}
BAD_DIR = {"runs","outputs","traces","checkpoints","__pycache__",".ipynb_checkpoints"}
def want(p):
    if not (p.startswith(("book/","docs/","skills/","chapter")) or p in
            {"README.md","README.en.md","LICENSE","mkdocs.yml","pyproject.toml",".gitignore"}): return False
    if p.split(".")[-1].lower() in BAD_EXT: return False
    if any(seg in BAD_DIR for seg in p.split("/")): return False
    if p.startswith("chapter10/book-translation/validation/"): return False
    return True
expected = {p for p in exp if want(p)}
disk = set()
for dp,_,fs in os.walk(R):
    if ".git" in dp.split(os.sep): continue
    for f in fs: disk.add(os.path.relpath(os.path.join(dp,f), R).replace("\\","/"))
missing = expected - disk
extra = disk - expected
print(f"期望 {len(expected)} 个 / 磁盘 {len(disk)} 个 / 缺失 {len(missing)} / 多余 {len(extra)}")
print("缺失按章分布:", Counter(p.split('/')[0] for p in missing).most_common())
print("缺失样例:", sorted(missing)[:12])
print("多余样例:", sorted(extra)[:6])
print("代码文件完整性: .py 期望 %d 实到 %d | .md 期望 %d 实到 %d" % (
    sum(1 for p in expected if p.endswith(".py")), sum(1 for p in disk if p.endswith(".py")),
    sum(1 for p in expected if p.endswith(".md")), sum(1 for p in disk if p.endswith(".md"))))
n = sum(len(fs) for dp,_,fs in os.walk(R) if ".git" not in dp.split(os.sep))
b = sum(os.path.getsize(os.path.join(dp,f)) for dp,_,fs in os.walk(R) if ".git" not in dp.split(os.sep)
        for f in fs if not _) if False else sum(os.path.getsize(os.path.join(dp,f)) for dp,_,fs in os.walk(R) if ".git" not in dp.split(os.sep) for f in fs)
print(f"工作区合计 {n} 文件 {b/1e6:.1f} MB")