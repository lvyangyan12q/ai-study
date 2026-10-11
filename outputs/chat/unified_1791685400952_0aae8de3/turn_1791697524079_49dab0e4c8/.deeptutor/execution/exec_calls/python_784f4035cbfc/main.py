import os, subprocess, glob, time, shutil

root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
BASE = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3")
NEW  = os.path.join(BASE, "turn_1791697524079_49dab0e4c8")
os.makedirs(NEW, exist_ok=True)

print("各 turn 目录内容:")
for d in sorted(glob.glob(os.path.join(BASE, "turn_*"))):
    print("  ", os.path.basename(d), os.listdir(d)[:6])

# 找到学习空间当前位置
cands = glob.glob(os.path.join(BASE, "turn_*/learning-space"))
print("learning-space 位置:", [os.path.basename(os.path.dirname(c)) for c in cands])
subprocess.run(["taskkill","/F","/IM","git.exe"], capture_output=True, text=True)
time.sleep(1)
src = cands[0]
LS  = os.path.join(NEW, "learning-space")
if os.path.abspath(src) != LS:
    try:
        os.rename(src, LS); print("已重命名迁移到最新目录")
    except OSError as e:
        print("rename 失败", e); shutil.copytree(src, LS, symlinks=True)

R = os.path.join(LS, "sources/ai-agent-book")
G = os.path.join(R, ".git")
print("仓库存在:", os.path.isdir(G))
for l in glob.glob(os.path.join(G, "**", "*.lock"), recursive=True):
    for a in range(3):
        try: os.remove(l); print("清锁:", os.path.basename(l)); break
        except Exception as e: time.sleep(2); print("锁仍在:", os.path.basename(l), type(e).__name__)

# 当前 sparse 状态与已检出内容
print("core.sparseCheckout =", subprocess.run(["git","config","core.sparseCheckout"],cwd=R,
      capture_output=True,text=True).stdout.strip())
sp = os.path.join(G,"info","sparse-checkout")
print("现有 sparse 规则:", open(sp,encoding="utf-8").read().replace("\n"," ") if os.path.exists(sp) else "(无)")
print("已检出顶层:", sorted(os.listdir(R))[:20])
print("解压后大小(MB):", round(sum(os.path.getsize(os.path.join(dp,f)) for dp,_,fs in os.walk(R) for f in fs)/1e6,1))

# 测代理速度
env = dict(os.environ); env["HTTPS_PROXY"]="http://127.0.0.1:7897"; env["HTTP_PROXY"]="http://127.0.0.1:7897"
tmp = os.path.join(LS,"_logs"); os.makedirs(tmp, exist_ok=True)
r = subprocess.run(["curl","-sL","--max-time","15","-o",os.path.join(tmp,"speedtest.tgz"),
     "-w","http=%{http_code} speed=%{speed_download} size=%{size_download}",
     "https://codeload.github.com/openai/openai-agents-python/tar.gz/refs/heads/main"],
     capture_output=True, text=True, env=env)
print("走代理 7897:", r.stdout.strip(), r.stderr.strip()[:200])