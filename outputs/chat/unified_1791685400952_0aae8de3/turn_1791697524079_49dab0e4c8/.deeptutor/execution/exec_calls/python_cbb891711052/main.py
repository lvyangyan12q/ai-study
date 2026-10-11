import os, subprocess, time, glob

root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
LS  = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791697524079_49dab0e4c8/learning-space")
R   = os.path.join(LS, "sources/ai-agent-book")
LOGD= os.path.join(LS, "_logs")
logpath = os.path.join(LOGD, "reapply.log")

env = dict(os.environ)
env["HTTPS_PROXY"] = env["HTTP_PROXY"] = "http://127.0.0.1:7897"
log = open(logpath, "w", encoding="utf-8", buffering=1)
p = subprocess.Popen(["git","-c","http.version=HTTP/1.1","-c","http.proxy=http://127.0.0.1:7897",
                      "-c","https.proxy=http://127.0.0.1:7897","-c","core.compression=6",
                      "sparse-checkout","reapply"],
                     cwd=R, env=env, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                     creationflags=0x00000008|0x00000200)
print("pid =", p.pid)
t0 = time.time()
while time.time()-t0 < 240:
    time.sleep(20)
    alive = p.poll() is None
    n = sum(len(fs) for _,_,fs in os.walk(R))
    mb = sum(os.path.getsize(os.path.join(dp,f)) for dp,_,fs in os.walk(R) for f in fs)/1e6
    tail = (open(logpath,encoding="utf-8",errors="replace").read().strip().splitlines() or [""])[-1]
    print(f"[{int(time.time()-t0):>3}s] 文件 {n:>5}  {mb:7.1f} MB  运行中={alive}  | {tail[:100]}")
    if not alive: break
print("退出码:", p.poll(), "耗时 %.0f s" % (time.time()-t0))
print("log 全文:", open(logpath,encoding="utf-8",errors="replace").read()[:400])
for d in sorted(glob.glob(os.path.join(R,"chapter*"))):
    n = sum(len(fs) for _,_,fs in os.walk(d))
    mb = sum(os.path.getsize(os.path.join(dp,f)) for dp,_,fs in os.walk(d) for f in fs)/1e6
    print(f"  {os.path.basename(d):<10} {n:>5} 文件 {mb:6.1f} MB")