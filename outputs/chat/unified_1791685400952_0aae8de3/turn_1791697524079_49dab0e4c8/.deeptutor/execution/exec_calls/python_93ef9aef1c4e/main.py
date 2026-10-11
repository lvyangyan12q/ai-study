import os, subprocess
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
LS  = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791697524079_49dab0e4c8/learning-space")
R   = os.path.join(LS, "sources/ai-agent-book")
log = open(os.path.join(LS,"_logs","reapply2.log"), encoding="utf-8", errors="replace").read()
errs = [l for l in log.splitlines() if l.startswith("error:")]
print("error 行数:", len(errs))
print("前 3 条:", errs[:3])
print("错误涉及的顶层目录分布:")
from collections import Counter
print(Counter(e.split("'")[1].split("/")[0] for e in errs if "'" in e))
print("非 'Filename too long' 的错误数量:", sum(1 for e in errs if "Filename too long" not in e))
print("\n规则文件当前内容:")
print(open(os.path.join(R,".git","info","sparse-checkout"),encoding="utf-8").read())
print("core.longpaths =", subprocess.run(["git","config","core.longpaths"],cwd=R,capture_output=True,text=True).stdout.strip())
print("git 版本:", subprocess.run(["git","--version"],capture_output=True,text=True).stdout.strip())

# 用 git 自己的 skip-worktree 标记判断哪些路径被排除(S=排除, H=在工作区)
out = subprocess.run(["git","ls-files","-t","-c","--","chapter10/book-translation/validation/"],
                     cwd=R, capture_output=True, text=True).stdout
print("\nchapter10/.../validation/ 的标记样本:", out.splitlines()[:3])
tags = Counter(l[0] for l in out.splitlines() if l.strip())
print("该目录标记统计:", tags)
for d in ["chapter2/attention_visualization/","chapter10/book-translation/"]:
    o = subprocess.run(["git","ls-files","-t","-c","--",d],cwd=R,capture_output=True,text=True).stdout
    print(d, Counter(l[0] for l in o.splitlines() if l.strip()))