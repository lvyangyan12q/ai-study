import os, subprocess
from collections import Counter
root = os.environ["DEEPTUTOR_WORKSPACE_ROOT"]
LS  = os.path.join(root, "outputs/chat/unified_1791685400952_0aae8de3/turn_1791697524079_49dab0e4c8/learning-space")
R   = os.path.join(LS, "sources/ai-agent-book")

# 1) 用 blob 直写，绕过 sparse 规则，恢复根文件
for p in ["pyproject.toml","mkdocs.yml","README.md","README.en.md","LICENSE",".gitignore","uv.lock"]:
    d = subprocess.run(["git","show",f"HEAD:{p}"],cwd=R,capture_output=True)
    if d.returncode==0:
        open(os.path.join(R,p),"wb").write(d.stdout)
print("根文件:", sorted(f for f in os.listdir(R) if os.path.isfile(os.path.join(R,f))))

# 2) 最终清点
def stat(d):
    n=py=0; b=0
    for dp,_,fs in os.walk(d):
        for f in fs:
            n+=1; py += f.endswith(".py")
            try: b += os.path.getsize(os.path.join(dp,f))
            except OSError: pass
    return n,py,b
rows=[]
for i in range(1,11):
    d=os.path.join(R,f"chapter{i}")
    if os.path.isdir(d):
        n,py,b=stat(d); rows.append((f"chapter{i}",n,py,b/1e6))
print(f"{'目录':<10}{'文件':>6}{'.py':>6}{'MB':>8}")
for r in rows: print(f"{r[0]:<10}{r[1]:>6}{r[2]:>6}{r[3]:>8.1f}")
for extra in ["book","docs","skills"]:
    d=os.path.join(R,extra)
    if os.path.isdir(d):
        n,py,b=stat(d); print(f"{extra:<10}{n:>6}{py:>6}{b/1e6:>8.1f}")
tot=stat(R); totpy_ok=subprocess.run(["git","ls-files","-c","--","*.py"],cwd=R,capture_output=True,text=True).stdout.count(".py")
print(f"合计 {tot[0]} 文件 / {tot[1]} 个 .py / {tot[2]/1e6:.1f} MB")
print("ch 顶层子目录示例 chapter2:", sorted(os.listdir(os.path.join(R,"chapter2")))[:12])

# 3) 生成清单
lines=["# 学习空间 · 克隆清单（bojieli/ai-agent-book）\n",
       f"本地源码：`sources/ai-agent-book/`　合计 {tot[0]} 文件 / {tot[1]} 个 Python 文件 / {tot[2]/1e6:.0f} MB\n",
       "| 目录 | 文件 | .py | 大小(MB) |","|---|---|---|---|"]
lines += [f"| {a} | {b} | {c} | {d:.1f} |" for a,b,c,d in rows]
lines += ["\n**已排除**：mp4/图片/PDF/音频（约 2000+ 个媒体文件）、runs/outputs/traces/checkpoints、*.jsonl/*.csv/*.log 等日志产物。需要某章演示素材时可按单文件补拉。",
          "**未取到**：83 个深层实验产物（chapter4/6 `validation/.../receipt.json`，Windows 路径超长限制），不影响代码运行。"]
open(os.path.join(LS,"00-克隆清单.md"),"w",encoding="utf-8").write("\n".join(lines))
print("清单已生成")