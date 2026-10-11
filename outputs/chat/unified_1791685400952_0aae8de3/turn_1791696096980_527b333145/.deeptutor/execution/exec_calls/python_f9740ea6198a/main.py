import os, subprocess, time, glob
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791696096980_527b333145")
R = os.path.join(NEW, "learning-space/sources/ai-agent-book")
G = os.path.join(R, ".git")

# 1) 查是否还有 git 进程在跑
p = subprocess.run(["tasklist","/FI","IMAGENAME eq git.exe","/FO","CSV"], capture_output=True, text=True)
print("running git:", p.stdout.strip()[-300:] if p.stdout else p.stderr[:200])

# 2) 清残锁
locks = glob.glob(os.path.join(G, "**", "*.lock"), recursive=True)
print("发现锁:", locks)
for l in locks:
    try: os.remove(l); print("  已删除:", os.path.basename(l))
    except Exception as e: print("  删除失败:", l, e)

def git(args, timeout=150):
    try:
        r = subprocess.run(["git"]+args, cwd=R, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "")[-300:], (r.stderr or "")[-300:].replace("\n"," ")
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", ""

print("状态:", git(["status","--short"])[:2])
t0=time.time()
rc, out, err = git(["-c","http.version=HTTP/1.1","sparse-checkout","add","chapter1"])
print("chapter1 rc:", rc, "用时:", round(time.time()-t0,1), "s", "| err:", err)
d = os.path.join(R,"chapter1")
print("chapter1 存在:", os.path.isdir(d), sorted(os.listdir(d))[:10] if os.path.isdir(d) else "-")