import os, subprocess, time
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791696096980_527b333145")
R = os.path.join(NEW, "learning-space/sources/ai-agent-book")

def du(p):
    total=0; files=0
    for dp,dn,fn in os.walk(p):
        if os.sep+".git" in dp: continue
        for f in fn:
            try: total+=os.path.getsize(os.path.join(dp,f)); files+=1
            except: pass
    return files, round(total/1024/1024,1)

def git(args, timeout=110):
    p = subprocess.run(["git"]+args, cwd=R, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stderr or "")[-200:].replace("\n"," ")

t_start = time.time()
done, failed = [], []
for ch in [f"chapter{i}" for i in range(1, 11)]:
    if time.time()-t_start > 235:
        print("...时间预算用尽，剩余章节留到下一批:", ch, "及之后"); break
    t0 = time.time()
    rc, err = git(["-c","http.version=HTTP/1.1","-c","http.postBuffer=524288000",
                   "sparse-checkout","add",ch])
    has = os.path.isdir(os.path.join(R, ch))
    print(f"{ch}: rc={rc} 目录存在={has} 用时={round(time.time()-t0,1)}s {err[:110]}")
    (done if rc == 0 else failed).append(ch)
print("成功:", done, "失败:", failed)
print("repo:", du(R))
print("已检出顶层:", sorted(d for d in os.listdir(R) if d.startswith("chapter")))