import os, shutil, subprocess
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
LS = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791687921332_2e58013d1c/learning-space")
SRC = os.path.join(LS, "sources")
a = os.path.join(SRC, "12-factor-agents"); b = os.path.join(SRC, "12-factor-agents-main")
if os.path.isdir(a) and set(os.listdir(a)) <= {".git"}:
    shutil.rmtree(a, ignore_errors=True)
if os.path.isdir(b) and not os.path.isdir(a): os.rename(b, a)
print("sources:", os.listdir(SRC))

R = os.path.join(SRC, "ai-agent-book")
t = open(os.path.join(R,"docs/zh-CN/LEARNING.md"), encoding="utf-8").read()
i = t.find("推荐的第一批")
print("---- 第一批实验 ----")
print(t[i:i+400])

def git(args):
    p = subprocess.run(["git"]+args, cwd=R, capture_output=True, text=True, timeout=200)
    return p.returncode, p.stdout, p.stderr

rc, out, err = git(["ls-tree","--name-only","HEAD"])
print("---- 顶层目录 ----"); print(rc, out.strip().replace("\n", "  "), err[-200:])
for ch in ["chapter2","chapter7"]:
    rc, out, err = git(["ls-tree","-r","--name-only","HEAD",ch+"/"])
    names = out.strip().split("\n") if out.strip() else []
    print(f"---- {ch}: {len(names)} 个文件, 顶层子目录:", sorted({n.split('/')[1] for n in names if '/' in n.split(ch+'/')[1] if len(n.split('/'))>2})[:16])