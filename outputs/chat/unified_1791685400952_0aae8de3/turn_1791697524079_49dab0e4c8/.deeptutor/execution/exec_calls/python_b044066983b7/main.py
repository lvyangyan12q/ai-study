import os, time, subprocess, glob

root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
LS  = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791697524079_49dab0e4c8/learning-space")
R   = os.path.join(LS, "sources/ai-agent-book"); LOGD = os.path.join(LS, "_logs")
logpath = os.path.join(LOGD, "reapply2.log")

def stat(d):
    n = 0; b = 0
    for dp,_ ,fs in os.walk(d):
        for f in fs:
            n += 1
            try: b += os.path.getsize(os.path.join(dp,f))
            except OSError: pass
    return n, b

def running():
    o = subprocess.run(["tasklist","/FI","IMAGENAME eq git.exe"], capture_output=True, text=True).stdout
    return "git.exe" in o

t0 = time.time()
while time.time()-t0 < 240:
    time.sleep(25)
    n, b = stat(R); alive = running()
    log = open(logpath,encoding="utf-8",errors="replace").read().strip()
    tail = (log.splitlines() or [""])[-1]
    print(f"[{int(time.time()-t0):>3}s] {n:>5} 文件 {b/1e6:7.1f} MB  git在跑={alive} | {tail[:95]}")
    if not alive:
        print("log 尾部:", log[-600:]); break

print("\n各章落盘情况:")
tot_n = tot_b = 0
for d in sorted(glob.glob(os.path.join(R,"chapter*")), key=lambda x:int(''.join(c for c in os.path.basename(x) if c.isdigit()))):
    n,b = stat(d); tot_n += n; tot_b += b
    print(f"  {os.path.basename(d):<10} {n:>5} 文件 {b/1e6:7.1f} MB")
print(f"  合计 {tot_n} 文件 {tot_b/1e6:.1f} MB（不含 .git）")