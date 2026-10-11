import os, subprocess, sys, json
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687921332_2e58013d1c")
LS = os.path.join(NEW, "learning-space")
SRC = os.path.join(LS, "sources")
os.makedirs(SRC, exist_ok=True)

def run(args, cwd, timeout=280):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "")[-1500:], (p.stderr or "")[-1500:]

repo = os.path.join(SRC, "ai-agent-book")
if not os.path.isdir(repo):
    rc, out, err = run(["git","clone","--depth","1","--filter=blob:none","--sparse",
                        "https://github.com/bojieli/ai-agent-book.git","ai-agent-book"], SRC)
    print("clone rc:", rc); print("err:", err[-400:])
    rc2, out2, err2 = run(["git","sparse-checkout","set","book","docs"], repo)
    print("sparse rc:", rc2); print("err2:", err2[-300:])

def du(p):
    total=0; files=0
    for dp,dn,fn in os.walk(p):
        for f in fn:
            fp=os.path.join(dp,f)
            try: total+=os.path.getsize(fp); files+=1
            except: pass
    return files, round(total/1024/1024,2)

print("repo:", du(repo))
print("book files:", sorted(os.listdir(os.path.join(repo,"book")))[:20])
print("docs:", os.path.join(repo,"docs"))
for dp,dn,fn in os.walk(os.path.join(repo,"docs")):
    print(" ", os.path.relpath(dp, repo), fn[:8])