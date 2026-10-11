import os, shutil, subprocess, time
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
OLD = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687804788_c528f60dea")
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791696096980_527b333145")
PREV = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687921332_2e58013d1c")
os.makedirs(NEW, exist_ok=True)

src_ls = os.path.join(PREV, "learning-space")
dst_ls = os.path.join(NEW, "learning-space")

def du(p):
    total=0; files=0
    for dp,dn,fn in os.walk(p):
        for f in fn:
            try: total+=os.path.getsize(os.path.join(dp,f)); files+=1
            except: pass
    return files, round(total/1024/1024,1)

t0=time.time()
if not os.path.isdir(dst_ls):
    shutil.copytree(src_ls, dst_ls, symlinks=True)
print("copied in", round(time.time()-t0,1), "s | prev:", du(src_ls), "new:", du(dst_ls))

SRC = os.path.join(dst_ls, "sources")
# 清理 12-factor-agents 的两个目录
a = os.path.join(SRC, "12-factor-agents"); b = os.path.join(SRC, "12-factor-agents-main")
if os.path.isdir(b):
    if os.path.isdir(a):
        for item in os.listdir(b):
            tgt = os.path.join(a, item)
            if os.path.exists(tgt):
                if os.path.isdir(tgt): shutil.rmtree(tgt, ignore_errors=True)
                else: os.remove(tgt)
            shutil.move(os.path.join(b, item), tgt)
        shutil.rmtree(b, ignore_errors=True)
    else:
        os.rename(b, a)
print("sources:", os.listdir(SRC))
for n in os.listdir(SRC):
    print("  ", n, du(os.path.join(SRC, n)))

# 稀疏检出：先加第 1-5 章实验代码
R = os.path.join(SRC, "ai-agent-book")
def git(args, timeout=270):
    p = subprocess.run(["git"]+args, cwd=R, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "")[-300:], (p.stderr or "")[-600:].replace("\n"," ")
t0=time.time()
rc, out, err = git(["sparse-checkout","add","chapter1","chapter2","chapter3","chapter4","chapter5"])
print("add ch1-5 rc:", rc, "| secs:", round(time.time()-t0,1), "| err:", err[-300:])
print("repo now:", du(R))