import os, subprocess, time
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
NEW = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791696096980_527b333145")
R = os.path.join(NEW, "learning-space/sources/ai-agent-book")

def git(args, timeout=200):
    p = subprocess.run(["git"]+args, cwd=R, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "")[-400:], (p.stderr or "")[-400:].replace("\n"," ")

print("sparse 当前配置:", git(["sparse-checkout","list"])[1:])
t0=time.time()
rc, out, err = git(["-c","http.version=HTTP/1.1","-c","pack.threads=1",
                    "sparse-checkout","add","chapter1"], timeout=200)
print("chapter1 rc:", rc, "用时:", round(time.time()-t0,1), "s")
print("stdout:", out); print("stderr:", err)
print("chapter1 目录存在:", os.path.isdir(os.path.join(R,"chapter1")))
if os.path.isdir(os.path.join(R,"chapter1")):
    print("内容:", sorted(os.listdir(os.path.join(R,"chapter1")))[:12])