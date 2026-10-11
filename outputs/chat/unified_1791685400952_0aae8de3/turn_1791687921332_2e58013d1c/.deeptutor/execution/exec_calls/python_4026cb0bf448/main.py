import os, io, tarfile, urllib.request, shutil, time
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687921332_2e58013d1c")
SRC = os.path.join(NEW, "learning-space/sources")

# 清掉上次中断留下的空仓库
bad = os.path.join(SRC, "12-factor-agents")
if os.path.isdir(bad):
    shutil.rmtree(bad, ignore_errors=True)

def fetch(owner_repo, branch="main", cap_mb=60):
    url = f"https://codeload.github.com/{owner_repo}/tar.gz/refs/heads/{branch}"
    t0 = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        buf = io.BytesIO()
        while True:
            chunk = r.read(262144)
            if not chunk: break
            buf.write(chunk)
            if buf.tell() > cap_mb*1024*1024: raise RuntimeError("exceeds cap")
            if time.time()-t0 > 180: raise RuntimeError("slow")
    buf.seek(0)
    name = owner_repo.split("/")[1]
    dest = os.path.join(SRC, name)
    if os.path.isdir(dest): shutil.rmtree(dest, ignore_errors=True)
    with tarfile.open(fileobj=buf, mode="r:gz") as tf:
        tf.extractall(SRC)
        top = tf.getnames()[0].split("/")[0]
    os.rename(os.path.join(SRC, top), dest)
    return round(buf.tell()/1024/1024,2), round(time.time()-t0,1)

for repo in ["humanlayer/12-factor-agents", "openai/openai-agents-python"]:
    ok = False
    for br in ["main", "master"]:
        try:
            mb, secs = fetch(repo, br)
            print(repo, "OK branch", br, mb, "MB in", secs, "s")
            ok = True; break
        except Exception as e:
            print(repo, br, "FAIL", type(e).__name__, str(e)[:120])
    if not ok: print(repo, "-> 放弃")

def du(p):
    total=0; files=0
    for dp,dn,fn in os.walk(p):
        if ".git" in dp: continue
        for f in fn:
            try: total+=os.path.getsize(os.path.join(dp,f)); files+=1
            except: pass
    return files, round(total/1024/1024,2)
print("sources:", os.listdir(SRC))
for n in os.listdir(SRC):
    print(" ", n, du(os.path.join(SRC,n)))